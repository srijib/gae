#!/usr/bin/env python
from google.appengine.ext import db
class Disk(db.Model):
    total = 1000*1000*1000
    host = db.LinkProperty(required = True)
    used = db.IntegerProperty(default = 0)
    active = db.BooleanProperty(default = True)
    time = db.DateTimeProperty(auto_now = True)
class FileRecord(db.Model):
    filename = db.StringProperty(required = True)
    url = db.LinkProperty(required = True)
    size = db.IntegerProperty(required = True)
    downloads = db.IntegerProperty(default = 0)
    tag = db.StringProperty(default = "")
    location = db.ReferenceProperty(Disk, required = True)
    time = db.DateTimeProperty(auto_now_add = True)
