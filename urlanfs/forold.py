# Copyright (C) 2010-2011 | GNU GPLv3
__author__ = 'd3d3LmVodXN0QGdtYWlsLmNvbQ=='.decode('base64')
__version__ = '0.4.2'

import gaeproxy
from gaeproxy import struct, zlib

class MainHandler(gaeproxy.MainHandler):
    _cfg = gaeproxy._init_config(gaeproxy.crypto.Crypto2)
    _cachename = 'wp_cache0'

    _unquote_map = {'0':'\x10', '1':'=', '2':'&'}
    def _quote(self, s):
        return str(s).replace('\x10', '\x100').replace('=','\x101').replace('&','\x102')
    def dump_data(self, dic):
        return '&'.join('%s=%s' % (self._quote(k), self._quote(v)) for k,v in dic.iteritems())
    def _unquote(self, s):
        res = s.split('\x10')
        for i in xrange(1, len(res)):
            item = res[i]
            try:
                res[i] = self._unquote_map[item[0]] + item[1:]
            except KeyError:
                res[i] = '\x10' + item
        return ''.join(res)
    def load_data(self, qs):
        pairs = zlib.decompress(qs).split('&')
        dic = {}
        for name_value in pairs:
            if not name_value:
                continue
            nv = name_value.split('=', 1)
            if len(nv) != 2:
                continue
            if len(nv[1]):
                dic[self._unquote(nv[0])] = self._unquote(nv[1])
        return dic

    def _pack_data(self, code, headers, data):
        ct = headers.get('Content-Type', '').lower()
        headers = self.dump_data(headers)
        info = struct.pack('>3I', code, len(headers), len(data))
        data = ''.join((info, headers, data))
        if ct.find('text')>=0 or ct.find('application')>=0:
            cdata = zlib.compress(data)
            data = '1'+cdata if len(data)>len(cdata) else '0'+data
        else:
            data = '0'+data
        return self._cfg['crypto'].encrypt(data, self._cfg['siteKey'])


def main():
    gaeproxy.run_main(MainHandler)

if __name__ == '__main__':
    main()
