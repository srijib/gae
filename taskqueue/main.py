from google.appengine.ext import webapp
from google.appengine.ext.webapp import util
from google.appengine.api.labs import taskqueue
import time

class MainHandler(webapp.RequestHandler):
  def get(self):
    taskurl = '/do'
    taskqueue.add( url='/do', method='GET', params=dict(url=taskurl))
    self.response.out.write("Task added!")
def main():
  application = webapp.WSGIApplication([('/.*', MainHandler)],  debug=True)
  util.run_wsgi_app(application)

if __name__ == '__main__':
  main()
