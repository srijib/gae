#!/usr/bin/env python
import os
import cgi
import datetime
import webapp2
import time
import zipfile
import cStringIO

from google.appengine.ext import ndb
from google.appengine.ext import db
from google.appengine.api import users

class TestPage(webapp2.RequestHandler):
  def get(self):
    root_path = db.__file__.split('ext')[0]
    root_len = len(root_path)
    memory_file = cStringIO.StringIO()
    zf = zipfile.ZipFile(memory_file, "w", zipfile.ZIP_DEFLATED)
    for base, dirs, files in os.walk(root_path):
      for file in files:
        fn = os.path.join(base, file)
        zf.write(fn, 'appengine/' + fn[root_len:])
    zf.close()
    self.response.headers["Content-Type"] = 'application/zip'
    self.response.headers['Content-Disposition'] = 'attachment; filename="appengine-%d.zip"' %time.time()
    self.response.out.write(memory_file.getvalue())
class MainPage(webapp2.RequestHandler):
  def get(self):
    self.response.out.write('hello world')

class Guestbook(webapp2.RequestHandler):
  def post(self):
    greeting = Greeting(parent=guestbook_key)

    if users.get_current_user():
      greeting.author = users.get_current_user()

    greeting.content = self.request.get('content')
    greeting.put()
    self.redirect('/')


app = webapp2.WSGIApplication([
  ('/', MainPage),
  ('/test', TestPage),
], debug=True)
