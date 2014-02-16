from google.appengine.ext import db
class Desktop(db.Model):
    name = db.StringProperty()
    pic = db.BlobProperty()
    time = db.DateTimeProperty( auto_now = True )
class Interval(db.Model):
    name = db.StringProperty()
    interval = db.IntegerProperty()
    time = db.DateTimeProperty( auto_now = True )