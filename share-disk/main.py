#!/usr/bin/env python
# -*- coding: utf-8 -*-
from google.appengine.ext import webapp
from google.appengine.ext.webapp import util
class MainHandler(webapp.RequestHandler):
    def get(self):
        self.response.out.write(u"""<h1><a href="upload">网盘</a></h1>""")
def main():
    application = webapp.WSGIApplication([('/.*', MainHandler)],
                                         debug=True)
    util.run_wsgi_app(application)


if __name__ == '__main__':
    main()
