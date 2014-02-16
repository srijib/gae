#!/usr/bin/env python

from google.appengine.ext import webapp
from google.appengine.ext import db
from google.appengine.ext.webapp import util
import StringIO
string = "abcdefghijklmnopqrstuvwxyz<br>"
class Huge(db.Model):
    data = db.BlobProperty()
    s = db.StringProperty(default="string")
    time = db.DateTimeProperty(auto_now = True)
def blob_data(MBs):
    global string
    return string*int(MBs*1024*1024/len(string))
class MainHandler(webapp.RequestHandler):
    def get(self):
        h = Huge()
        MBs = self.request.get("MBs") or "0.001"
        MBs = float(MBs)
        d = StringIO.StringIO()
        d.seek(int(MBs*1024*1024-1))
        d.write("\0")
        h.data = d.getvalue()
        #h.data = blob_data(MBs)
        h.put()
        self.response.out.write("ok")
def main():
    application = webapp.WSGIApplication([('/datastore', MainHandler)],
                                         debug=True)
    util.run_wsgi_app(application)


if __name__ == '__main__':
    main()
