from google.appengine.ext import webapp
from google.appengine.ext.webapp import util
from google.appengine.ext import db
import datetime, cgi, re
class File(db.Model):
  fid = db.IntegerProperty()
  parts = db.IntegerProperty()
  url = db.StringProperty()
  filename = db.StringProperty()
  filesize = db.IntegerProperty()
  time = db.DateTimeProperty(auto_now_add=True)

class FilePart(db.Model):
  fid = db.IntegerProperty()
  url = db.StringProperty()
  filename = db.StringProperty()
  part = db.IntegerProperty()
  bin = db.BlobProperty()
  time = db.DateTimeProperty(auto_now=True)

class MainHandler(webapp.RequestHandler):
  def get(self):
    fid = self.request.get('fid')
    part = self.request.get('part')
    single = self.request.get('single')
    if fid and part:
      fileparts = db.GqlQuery("SELECT * FROM FilePart WHERE fid=%s AND part=%s" %(fid, part))
      filepart = fileparts.get()
      self.response.headers['Content-Type'] = 'application/octet-stream'
      if single:
        self.response.headers['Content-Disposition'] = "attachment; filename=%s" % (filepart.filename)
      else:
        self.response.headers['Content-Disposition'] = "attachment; filename=%s" % (filepart.filename+"."+str(part))
      self.response.out.write(filepart.bin)
    else:
      #    self.response.headers['Content-Type'] = 'text/html'
      #    self.response.out.write(u"This File Not Found!")
      pass

def main():
  application = webapp.WSGIApplication([('/.*', MainHandler)],
                                       debug=True)
  util.run_wsgi_app(application)

if __name__ == '__main__':
  main()
