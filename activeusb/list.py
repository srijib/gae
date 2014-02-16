#!/usr/bin/env python
#-*- coding: utf-8 -*-

from google.appengine.ext import webapp
from google.appengine.ext.webapp import util
from model import Code
class ListHandler(webapp.RequestHandler):
    def get(self):
        self.response.out.write("<h1>Code List</h1>")
        self.response.out.write("""<p>Write your code. <a href="/edit">Start here</a></p>""")
        codes = Code.all()
        ncode = codes.count()
        for code in codes:
            self.response.out.write("""<li>%s <a href="/edit/%s">%s</a></li>""" %(code.add_time, code.name, code.name ))
            self.response.out.write("<br>")
        self.response.out.write("Total: %d<br>" %ncode)

def list_main():
    application = webapp.WSGIApplication([('/.*', ListHandler)],
                                         debug=True)
    util.run_wsgi_app(application)



if __name__ == '__main__':
    list_main()
