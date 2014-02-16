#-*- coding: utf-8 -*-
#!/usr/bin/env python

from google.appengine.ext import webapp
from google.appengine.ext.webapp import util
#print dir(),1
class Handler(webapp.RequestHandler):
    #print dir(),2
    def get(self):
        print dir(),3
        self.response.out.write('Hello world!')
        execfile("project_01.py")
        print dir(),8
        code = open("sobad.py").read()
        exec(compile(code,"nn","exec"))
class Handler2(webapp.RequestHandler):
    def get(self):
        code = open("sobad.py").read()
        exec(compile(code,"nn","exec"))
        
def mmm():
    application = webapp.WSGIApplication([('/project_handler.*', Handler),('/sobad', Handler2)],
                                         debug=True)
    util.run_wsgi_app(application)
    print dir(),9

if __name__ == '__main__':
    mmm()
