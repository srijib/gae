# encoding: utf-8
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
import logging
import urllib2
def cbk(blocks_read, block_size, total_size):  
    if not blocks_read:  
        logging.info('Connection opened')  
    if total_size < 0:  
        logging.info('Read %d blocks' % blocks_read)  
    else:
        logging.info('blocks_read:%d, block_size:%d, totalsize:%d Bytes' % (blocks_read, block_size, total_size))
class TestHandler(webapp.RequestHandler):
    def get(self):
        url = 'http://ftp.sjtu.edu.cn/ubuntu/ubuntu/dists/quantal/main/binary-i386/Packages.gz'
        logging.info(tmp)
        result = urllib2.urlopen(url = url)
        result.read(1024)
        self.response.out.write('ok')
class BackendHandler(webapp.RequestHandler):
    def get(self):
        from google.appengine.api import taskqueue
        logging.info('BackendHandler GET function called.')
        try:
            logging.info('working expensive start')
            # do something expensive
            while True:
                pass
        except:
            logging.info('in exception start')
            taskqueue.add(url='/backend', method='GET')
            logging.info('in exception end')
        logging.info('outside exception')
app = webapp.WSGIApplication([
    ('/test', TestHandler),
    ('/backend', BackendHandler),
    ], debug=True)
def main():
    run_wsgi_app(app)
if __name__ == "__main__":
    main()
