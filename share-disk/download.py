#!/usr/bin/env python

from google.appengine.ext import webapp
from google.appengine.ext.webapp import util
from models import *

class MainHandler(webapp.RequestHandler):
    def get(self):
        key = self.request.get("key")
        if not key:
            return
        file = File.get(key)
        import mimetypes
        mime = mimetypes.guess_type(file.filename)
        mime = mime[0] or "application/octet-stream"
        self.response.headers['Content-Type'] = mime
        import urllib
        self.response.headers['Content-Disposition'] = "attachment; filename=%s" % urllib.quote(file.filename.encode("utf8"))
        node = file.head.next
        while node:
            self.response.out.write(node.data)
            node = node.next
def main():
    application = webapp.WSGIApplication([('/download', MainHandler)],
                                         debug=True)
    util.run_wsgi_app(application)


if __name__ == '__main__':
    main()
