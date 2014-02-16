# encoding: utf-8
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
import logging
class CleanHandler(webapp.RequestHandler):
    def get(self):
        self.response.out.write("""<form action="/clean" method="post"><input type="submit" value="是的,我真的要把数据库全部清空" /></form>""")
    def post(self):
        from google.appengine.ext import db
        from model import File, FileBlock
        db.delete(db.GqlQuery('SELECT __key__ FROM File'))
        db.delete(db.GqlQuery('SELECT __key__ FROM FileBlock'))
        logging.warn('!!!datastore clear action!!!')
        self.response.out.write("DB cleared!")
app = webapp.WSGIApplication([
    ('/clean', CleanHandler),
    ], debug=True)
def main():
    run_wsgi_app(app)
if __name__ == "__main__":
    main()
