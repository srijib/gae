#!/usr/bin/env python

from google.appengine.ext import webapp
from google.appengine.ext.webapp import util
string = "abcdefghijklmnopqrstuvwxyz<br>"
def flush(self, MBs):
    global string
    self.response.out.write(string*int(MBs*1024*1024/len(string)))
class MainHandler(webapp.RequestHandler):
    def get(self):
        MBs = float(self.request.get("MBs"))
        flush(self, MBs)

def main():
    application = webapp.WSGIApplication([('/response', MainHandler)],
                                         debug=True)
    util.run_wsgi_app(application)


if __name__ == '__main__':
    main()
