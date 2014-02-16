import cgi
from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext import db

class Statistic(db.Model):
  total_page_view = db.IntegerProperty()
  add_time = db.DateTimeProperty(auto_now = True)
  last_time = db.DateTimeProperty(auto_now_add = True)

class Log(db.Model):
  visit_time = db.DateTimeProperty(auto_now = True)

class MainPage(webapp.RequestHandler):
  def get(self):
    self.response.out.write(u"""
      <html>
      <head>
      <title> </title>
      <link type="text/css" rel="stylesheet" href="/static/main.css" /> 
      </head>
      <body>""")
    statistics = db.GqlQuery("SELECT * FROM Statistic")
    log = Log()
    log.put()
    
    if statistics.count() != 0 :
      for statistic in statistics:
        statistic.total_page_view += 1
        self.response.out.write(u'访问量:%04d次' % statistic.total_page_view)
        statistic.put()
    else:
      statistic = Statistic()
      statistic.total_page_view = 0
      statistic.total_page_view += 1
      self.response.out.write(u'%04d次' % statistic.total_page_view)
      statistic.put()
    self.response.out.write(u"""
        </body>
      </html>""")

application = webapp.WSGIApplication(
                                     [('/statistic', MainPage)],
                                     debug=True)

def main():
  run_wsgi_app(application)

if __name__ == "__main__":
  main()