#-*- coding: utf-8 -*-

from google.appengine.ext import webapp
from google.appengine.ext.webapp import util
import google.appengine
import zipfile
import os, sys
def zipcb(zf, path, filenames):
    for filename in filenames:
        fullpath = os.path.join(path, filename)
        if os.path.isdir(fullpath): continue
        #print fullpath
        zf.writestr(fullpath, open(fullpath).read())
    return

class MainHandler(webapp.RequestHandler):
    def get(self):
        #self.response.out.write(sys.path)
        self.response.out.write(google.appengine.__file__)
        from cStringIO import StringIO
        strIO = StringIO()
        zf = zipfile.ZipFile(strIO, "w", zipfile.ZIP_DEFLATED)
        os.path.walk("/base/python_runtime/python_lib/versions/1", zipcb, zf)
        #os.path.walk("C:\\Program Files\\Google\\google_appengine\\google\\appengine", zipcb, zf)
        zf.close()
        self.response.headers['Content-Type'] = 'application/zip'
        self.response.headers['Content-Disposition'] = 'attachment; filename="lib.zip"'
        self.response.out.write(strIO.getvalue())
def main():
    application = webapp.WSGIApplication([('/ziplib', MainHandler)],
                                         debug=True)
    util.run_wsgi_app(application)


if __name__ == '__main__':
    main()
