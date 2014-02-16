from google.appengine.ext import webapp
from google.appengine.ext.webapp import util
from google.appengine.api.labs import taskqueue
from google.appengine.api import urlfetch
import time

class MainHandler(webapp.RequestHandler):
  def get(self):
    time_str = time.strftime('%Y-%m-%d %X', time.gmtime( time.time() ) )
    self.response.out.write(time_str)
    url = "https://sms.api.bz/fetion.php?username=13821254203&password=snowmanshan0913&sendto=13821254203&message=" + time_str.encode("utf-8").replace(" ","%20")
    result = urlfetch.fetch(url)
    if result.status_code == 200:
      self.response.out.write('Sent OK! ')
    else:
      self.response.out.write('Failed. ')
def main():
  application = webapp.WSGIApplication([('/do', MainHandler)],
                                       debug=True)
  util.run_wsgi_app(application)

if __name__ == '__main__':
  main()
