#!/usr/bin/python
# -*- coding: utf-8 -*-
from google.appengine.ext import webapp
from google.appengine.ext.webapp import util
from google.appengine.api import urlfetch
import re
class MainHandler(webapp.RequestHandler):
  def get(self):
    url="http://www.baidu.com"
    result = urlfetch.fetch(url)
    if result.status_code == 200:
      #print result.content
      self.response.out.write(result.content)
    else:
      self.response.out.write('My error!')
def main():
  application = webapp.WSGIApplication([('/', MainHandler)],
                                       debug=True)
  util.run_wsgi_app(application)

if __name__ == '__main__':
  main()