from google.appengine.ext import webapp
from google.appengine.ext.webapp import util
from google.appengine.ext import db
class Comment(db.Model):
  name = db.StringProperty()
  content = db.StringProperty(multiline=True)
  ref = db.SelfReferenceProperty()
  time = db.DateTimeProperty(auto_now_add=True)
class MainHandler(webapp.RequestHandler):
  def get(self):
    comment1 = Comment(name="user1",content ="comment1")
    comment1.put()
    comment2 = Comment(name="user2",content ="comment2",ref = comment1)
    comment2.put()
    comment3 = Comment(name="user3",content ="comment3",ref = comment2)
    comment3.put()
    
    self.response.out.write(u'end.')


def main():
  application = webapp.WSGIApplication([('/', MainHandler)],
                                       debug=True)
  util.run_wsgi_app(application)


if __name__ == '__main__':
  main()
