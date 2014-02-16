from google.appengine.ext import db

class Task(db.Model):
    name = db.StringProperty()
    url = db.LinkProperty(required = True)
    enabled = db.BooleanProperty(default = True)
    time = db.DateTimeProperty(auto_now_add = True)
class Result(db.Model):
    Tile = 1
    Toast = 2
    Raw = 3
    
    task = db.ReferenceProperty(required = True)
    type = db.IntegerProperty()
    
    request_headers = db.TextProperty()
    request_content = db.TextProperty()
    
    response_headers = db.TextProperty()
    response_content = db.TextProperty()
    response_code = db.IntegerProperty()
    
    subscription_status = db.StringProperty()
    deviceconnection_status = db.StringProperty()
    notification_status = db.StringProperty()
    
    ok = db.BooleanProperty(required = True)
    info = db.StringProperty()
    time = db.DateTimeProperty(auto_now_add = True)
