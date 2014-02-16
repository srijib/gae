# encoding: utf-8
from google.appengine.ext import db

class File(db.Model):
    name = db.StringProperty(multiline=False)
    author = db.UserProperty()
    content = db.TextProperty()
    add_time = db.DateTimeProperty(auto_now_add=True)
    time = db.DateTimeProperty(auto_now=True)
