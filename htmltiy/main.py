from google.appengine.ext import webapp
from google.appengine.ext.webapp import util
from google.appengine.api import urlfetch

class view(webapp.RequestHandler):
  def get(self):
    self.response.out.write('HTML Try It Yourself')

  def post(self):
    self.response.out.write(self.request.get("c"))

class url(webapp.RequestHandler):
  def post(self):
    #self.response.out.write(self.request.get("c"))
    url = self.request.get('url')
    data = urlfetch.fetch(url = url)
    if 200 <= data.status_code < 300:
       self.response.out.write("HTML(please remove comment):<br /><textarea rows='40' cols='120'><!--\n"+data.content+"\n--></textarea>")
def main():
  application = webapp.WSGIApplication([('/v', view),('/u', url)],
                                       debug=True)
  util.run_wsgi_app(application)


if __name__ == '__main__':
  main()
