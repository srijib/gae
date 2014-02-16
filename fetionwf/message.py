import cgi

from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext import db

class Greeting(db.Model):
  author = db.StringProperty()
  content = db.StringProperty(multiline=True)
  date = db.DateTimeProperty(auto_now_add=True)

class MainPage(webapp.RequestHandler):
  def get(self):
    self.response.out.write("""
      <html>
      <head>
      <title>Message</title>
      <link type="text/css" rel="stylesheet" href="/static/main.css" /> 
      </head>
      <body>""")
    # Write the submission form and the footer of the page
    self.response.out.write(u"""
          <h1>Message Board</h1>
          <table>
          <form action="/message/leave" method="post">
          <tr><td>大名:</td><td align="left"><input type="text" name="author" ></input></td><td align="right">
            <input type="submit" value="提交"></td></tr>
          <tr><td>留言:</td><td colspan="2"><textarea name="content" rows="4" cols="24"></textarea></td></tr>
          </form>
          </table><br>""")

    greetings = db.GqlQuery("SELECT * FROM Greeting ORDER BY date ASC")

    for greeting in greetings:
      if greeting.author:
        self.response.out.write('<b>%s</b> wrote:' % cgi.escape(greeting.author))
      else :
        self.response.out.write('<b>%s</b> wrote:' % "An anonymous person" )
      self.response.out.write('<blockquote>%s</blockquote>' %
                              cgi.escape(greeting.content))
    self.response.out.write(u"""
        <a href = "/">返回主页</a>
        </body>
      </html>""")
class Guestbook(webapp.RequestHandler):
  def post(self):
    greeting = Greeting()

    greeting.content = self.request.get('content')
    greeting.author = self.request.get('author')
    if greeting.content and greeting.author :
      greeting.put()
    self.redirect('/message')

application = webapp.WSGIApplication(
                                     [('/message', MainPage),
                                      ('/message/leave', Guestbook)],
                                     debug=True)

def main():
  run_wsgi_app(application)

if __name__ == "__main__":
  main()