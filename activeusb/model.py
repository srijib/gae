#-*- coding: utf-8 -*-
#!/usr/bin/env python

from google.appengine.ext import db

class Code(db.Model):
    language = db.StringProperty()
    name = db.StringProperty(required = True)
    code = db.TextProperty(required = True)
    add_time = db.DateTimeProperty(auto_now_add = True)
    mod_time = db.DateTimeProperty(auto_now = True)
    