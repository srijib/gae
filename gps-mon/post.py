from google.appengine.ext import webapp
from google.appengine.ext.webapp import util
from google.appengine.ext import db
import time, datetime
#/post?id=0&latitude=0.00&longitude=0.00&name=your_name&time=1271768981.0
class GpsData(db.Model):
  
  name = db.StringProperty()					#name
  id = db.IntegerProperty()					#id
  location = db.ListProperty(db.GeoPt)							#GPS位置
  server_time = db.ListProperty(datetime.datetime)		#服务器获得时间
  phone_time = db.ListProperty(datetime.datetime)		#手机时间

class MainHandler(webapp.RequestHandler):

  def get(self):
    self.response.out.write(self.request.query_string)
    id = self.request.get('id')
    if id:
      gpsdatas = db.GqlQuery("SELECT * FROM GpsData WHERE id=%s" % id)
      if not gpsdatas.count():
        data = GpsData()
        data.id = int(id)
        data.location = []
        data.server_time = []
        data.phone_time = []
      else:
        data = gpsdatas.get()
      #common refresh action below
      data.name = self.request.get('name')
      lat, long = self.request.get('latitude'), self.request.get('longitude')
      if lat and long:
        data.location.append( db.GeoPt(float(lat), float(long)) )
        data.server_time.append( datetime.datetime.now() )
        phone_time = self.request.get('time')
        if phone_time:
          try:
            data.phone_time.append( datetime.datetime(*time.gmtime(float(phone_time))[0:7]) )
          except:
            data.phone_time.append( datetime.datetime.now() )
        else:
          data.phone_time.append( datetime.datetime.now() )
      else:
        self.response.out.write("Wrong request format: need latitude & longitude")
      data.put()
    else:
      self.response.out.write("Wrong request format: need id")
def main():
  application = webapp.WSGIApplication([('/.*', MainHandler)],
                                       debug=True)
  util.run_wsgi_app(application)


if __name__ == '__main__':
  main()
