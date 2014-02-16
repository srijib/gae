#-*- coding: utf-8 -*-
#!/usr/bin/env python
from google.appengine.ext import webapp
from google.appengine.ext.webapp import util
#print dir(),4
class MainHandler(webapp.RequestHandler):
    #print "aa"
    #print dir(),5
    def get(self):
        self.response.out.write('project01')
#print dir(),6
class MainHandler2(webapp.RequestHandler):
    def get(self):
        self.response.out.write('project02')

def mm():
    """application = webapp.WSGIApplication([('/project_handler', MainHandler),('/project_handler2', MainHandler2)],
                                         debug=True)
    util.run_wsgi_app(application)"""
    print dir(),7
    pass
print __name__
if __name__ == '__main__':
    mm()
