# encoding: utf-8
from google.appengine.ext import db
class EStatus:
    ERROR = -1
    IDLE = 0
    DOWNLOADING = 1
    DONE = 2
class File(db.Model):
    name = db.StringProperty(multiline = False)
    url = db.LinkProperty()
    downloader = db.UserProperty()
    size = db.IntegerProperty()
    mimetype = db.StringProperty(multiline = False)
    status = db.IntegerProperty(default = EStatus.IDLE)
    add_time = db.DateTimeProperty(auto_now_add = True)
    time = db.DateTimeProperty(auto_now = True)
class FileBlock(db.Model):
    file = db.ReferenceProperty(File)
    n = db.IntegerProperty()
    content = db.BlobProperty()
    add_time = db.DateTimeProperty(auto_now = True)