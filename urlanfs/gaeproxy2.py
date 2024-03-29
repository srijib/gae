# Copyright (C) 2010-2011 | GNU GPLv3
__author__ = 'd3d3LmVodXN0QGdtYWlsLmNvbQ=='.decode('base64')
__version__ = '1.0.7'

from util import crypto, httpheaders
import cPickle as pickle
import zlib, logging, time, re, struct
from google.appengine.ext import webapp, db
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.api import urlfetch, memcache
from google.appengine.runtime import apiproxy_errors
urlfetch._CaselessDict = httpheaders.HTTPHeaders

class WPConfig(db.Model):
    cfgCacheTime = db.IntegerProperty(required=True, default=5*60)
    cacheTime = db.IntegerProperty(default=24*3600)
    maxSize = db.IntegerProperty(required=True, default=9000000)
    mixSize = db.IntegerProperty(default=100000)
    siteKey = db.StringProperty(default=u'')
    cryptoMode = db.StringProperty(default=u'XOR--32')
    version = db.StringProperty()

def getConfig():
    config = memcache.get('config', namespace='wp_config')
    if config is None:
        cfg = WPConfig.all().get()
        if not cfg:#No Entry
            cfg = WPConfig(version=__version__)
            cfg.put()
        elif cfg.version < __version__:
            cfg = WPConfig(key=cfg.key(), siteKey=cfg.siteKey,
                    cryptoMode=cfg.cryptoMode, version=__version__)
            cfg.put()
            memcache.flush_all()
        config = {'cacheTime':cfg.cacheTime, 'maxSize':cfg.maxSize,
                  'siteKey':cfg.siteKey.encode('utf-8').decode('string_escape'),
                  'crypto':cfg.cryptoMode.encode('utf-8'), 'mixSize':cfg.mixSize}
        if not memcache.set('config', config, cfg.cfgCacheTime, namespace='wp_config'):
            logging.error('Memcache set wp_config failed')
    return config

def _init_config(crypto_cls):
    config = getConfig()
    config['crypto'] = crypto_cls(config['crypto'])
    return config

class MainHandler(webapp.RequestHandler):
    _cfg = _init_config(crypto.Crypto)
    _dirty_headers = ('X-Google-Cache-Control', 'Via')
    _setcookie_re = re.compile(r', ([^ =]+(?:=|$))')
    _crange_re = re.compile(r'bytes\s+(\d+)-(\d+)/(\d+)')
    _try_times = 2
    _deadline = (5, 10)
    _cachename = 'wp_cache'

    def dump_data(self, data):
        return pickle.dumps(data, 1)

    def load_data(self, data):
        return pickle.loads(zlib.decompress(data))

    def _need_cache(self, method, code, headers):
        need_cache = False
        if (method=='GET' and code==200 and self._cfg['cacheTime'] and
            headers.get('Content-Type', '').lower().find('text/html')<0 and
            headers.get('Pragma', '').find('no-cache')<0 and
            headers.get('Cache-Control', '').find('no-cache')<0 and
            'Set-Cookie' not in headers):
            t = time.gmtime(time.time() + self._cfg['cacheTime'])
            headers['X-Cache'] = 'HIT from WallProxy'
            headers['Expires'] = time.strftime('%a, %d %b %Y %H:%M:%S GMT', t)
            headers['Cache-Control']='public, max-age=%d'%self._cfg['cacheTime']
            t = time.strftime('%a, %d %b %Y %H:%M:%S GMT', time.gmtime())
            headers['Last-Modified'] = t
            need_cache = True
        return need_cache

    def _pack_data(self, code, headers, data):
        crypto = self._cfg['crypto']
        ct = headers.get('Content-Type', '').lower()
        headers = self.dump_data(headers.__getstate__())
        zip = 0
        if ct.find('text')>=0 or ct.find('application')>=0:
            cdata = crypto.paddata(zlib.compress(headers+data))
            if len(cdata) < (crypto.getsize(len(headers)) +
                             crypto.getsize(len(data))): zip = 1
        if zip == 0:
            headers = crypto.paddata(headers)
            data = crypto.paddata(data)
        info = struct.pack('>BHI', zip, code, len(headers))
        crypto = crypto.getcrypto(self._cfg['siteKey'])
        if zip == 1: return info + crypto.encrypt(cdata)
        return '%s%s%s' % (info, crypto.encrypt(headers), crypto.encrypt(data))

    def _send_data(self, data, length):
        self.response.headers['Content-Type'] = 'application/octet-stream'
        self.response.headers['Content-Length'] = str(length)
        self.response.out.write(data)

    def sendResponse(self, code, headers, content, method, url):
        need_cache = self._need_cache(method, code, headers)
        data = self._pack_data(code, headers, content)
        length = len(data)
        if need_cache and length<1000000:
            try:
                if not memcache.set(url, data, self._cfg['cacheTime'], namespace=self._cachename):
                    logging.warning('Memcache set %s(%s) failed' % (self._cachename, url))
            except: pass
        if code == 555:
            logging.warning('Response: "%s %s" %s' % (method, url, content))
        else:
            logging.debug('Response: "%s %s" %d %d/%d' % (
                          method, url, code, len(content), length))
        self._send_data(data, length)

    def sendNotify(self, code, content, method='', url='', fullContent=False):
        if not fullContent and code!=555:
            content = ('<h2>Fetch Server Info</h2><hr noshade="noshade">'
                    '<p>Code: %d</p><p>Message: %s</p>' % (code, content))
        headers = httpheaders.HTTPHeaders({'Server':'WallProxy/%s'%__version__,
                'Content-Type':'text/html', 'Content-Length':len(content)})
        self.sendResponse(code, headers, content, method, url)

    def handle_wallproxy(self, method, url):
        import os
        appid = '%s v%s' % (os.environ['APPLICATION_ID'],
                            os.environ['CURRENT_VERSION_ID'])
        path = url[len('http://wallproxy'):].lower()
        if path == '/cache':
            resp = ('<h2>Memcache Status(%s)</h2><hr noshade="noshade">'
                    '<p>%s</p>' % (appid, memcache.get_stats()))
            return self.sendNotify(200, resp, method, url, True)
        elif path == '/cache/reset' and memcache.flush_all():
            crypto_cls = self._cfg['crypto'].__class__
            self.__class__._cfg = _init_config(crypto_cls) #reset password
            return self.sendNotify(200, 'Memcache Reseted(%s)'%appid,method,url)
        else:
            resp = []
            for k,v in self._cfg.iteritems():
                resp.append('%s: %s' % (k, v))
            resp = ('<h2>WallProxy Configuration(%s)</h2><hr noshade="noshade">'
                    '<pre>%s</pre>' % (appid, '\n'.join(resp)))
            return self.sendNotify(200, resp, method, url, True)

    def _check_cache(self, method, url, headers):
        data = None
        if self._cfg['cacheTime'] and method=='GET':
            data = memcache.get(url, namespace=self._cachename)
        if data is not None:
            if 'If-Modified-Since' in headers:
                headers = httpheaders.HTTPHeaders()
                self.sendResponse(304, headers, '', method, url)
            else:
                length = len(data)
                logging.debug('Memcache hits: "%s %s" %d %d' % (method, url, 200, length))
                self._send_data(data, length)
            return True
        return False

    def _check_headers(self, respheaders):
        for k in self._dirty_headers:
            del respheaders[k]
        if 'Set-Cookie' in respheaders:
            respheaders['Set-Cookie'] = self._setcookie_re.sub(
                r'\r\nSet-Cookie: \1', respheaders['Set-Cookie'])

    def _check_resplength(self, resp):
        max_size = self._cfg['maxSize']
        if 500000 < max_size < len(resp.content):
            m = self._crange_re.search(resp.headers.get('Content-Range', ''))
            if m:
                m = m.groups()
                start=int(m[0]); end=start+max_size-1; whole=int(m[2])
            else:
                start=0; end=max_size-1; whole=len(resp.content)
            resp.status_code = 206
            resp.headers['Content-Range'] = 'bytes %d-%d/%d' % (start, end, whole)
            resp.content = resp.content[:max_size]
        resp.headers['Content-Length'] = len(resp.content)

    def post(self):
        try:
            request = self._cfg['crypto'].decrypt(self.request.body,
                        self._cfg['siteKey'])
            request = self.load_data(request)
        except:
            return self.response.out.write('Hello World!')
        method = request.get('method', '')
        if not hasattr(urlfetch, method):
            return self.sendNotify(555, 'Invalid Method', method)
        fetch_method = getattr(urlfetch, method)
        url = request.get('url', '')
        # modified here
        # @@@ location here @@@
        location_url = "http://www.baidu.com"
        if location_url in url:
            already_redir = True
        else:
            url = location_url
            already_redir = False
        # end of modify
        if not url.startswith('http'):
            return self.sendNotify(555, 'Unsupported Scheme', method, url)
        if url.startswith('http://wallproxy/'):
            return self.handle_wallproxy(method, url)
        headers = request.get('headers', '')
        if isinstance(headers, str):
            headers = httpheaders.HTTPHeaders(headers)
        headers['Connection'] = 'close'
        range = request.get('range')
        if range and self._check_cache(method, url, headers): return
        body = request.get('payload')
        deadline = self._deadline[1 if body else 0]
        for i in xrange(self._try_times):
            try:
                resp = urlfetch.fetch(url, body, fetch_method,
                                      headers, False, False, deadline)
                break
            except apiproxy_errors.OverQuotaError, e:
                time.sleep(2)
            except urlfetch.InvalidURLError, e:
                return self.sendNotify(555, 'Invalid URL: %s' % e, method, url)
            except urlfetch.ResponseTooLargeError, e:
                if method == 'GET':
                    deadline = self._deadline[1]
                    if range: headers['Range'] = range
                else:
                    return self.sendNotify(555, 'Response Too Large: %s' % e, method, url)
            except Exception, e:
                if i==0 and method=='GET':
                    deadline = self._deadline[1]
                    if range: headers['Range'] = range
        else:
            return self.sendNotify(555, 'Urlfetch error: %s' % e, method, url)
        if not already_redir:
            resp.status_code = 302
            resp.content = ""
            resp.headers["Location"] = "http://www.baidu.com"
        self._check_headers(resp.headers)
        self._check_resplength(resp)
        return self.sendResponse(resp.status_code, resp.headers, resp.content, method, url)

    def get(self):
        self.redirect('http://twitter.com/hexieshe')

def run_main(cls):
    run_wsgi_app(webapp.WSGIApplication([(r'/.*', cls)], debug=True))

def main():
    run_main(MainHandler)

if __name__ == '__main__':
    main()
