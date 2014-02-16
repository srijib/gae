# Copyright (C) 2010-2011 | GNU GPLv3
__author__ = 'ZHRtYWppYUAxNjMuY29t'.decode('base64')
__version__ = '0.0.1'

import gaeproxy, marshal, struct

class MainHandler(gaeproxy.MainHandler):
    _cachename = 'wp_cache3'

    def dump_data(self, data):
        return marshal.dumps(tuple((k,str(v)) for k,v in data.iteritems()))

    def load_data(self, data):
        return dict(marshal.loads(data))

    def _pack_data(self, code, headers, data):
        crypto = self._cfg['crypto']
        headers = str(headers)
        if len(data) <= self._cfg['mixSize']:
            info = struct.pack('>BHI', 1, code, len(headers))
            return info + crypto.encrypt(headers+data, self._cfg['siteKey'])
        headers = crypto.paddata(headers)
        data = crypto.paddata(data)
        info = struct.pack('>BHI', 0, code, len(headers))
        crypto = crypto.getcrypto(self._cfg['siteKey'])
        return '%s%s%s' % (info, crypto.encrypt(headers), crypto.encrypt(data))


def main():
    gaeproxy.run_main(MainHandler)

if __name__ == '__main__':
    main()
