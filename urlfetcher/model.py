from google.appengine.ext import db
class Data(db.Model):
    url = db.LinkProperty(required = True)
    alive = db.BooleanProperty(required = True)
    