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
    files = db.GqlQuery("SELECT * FROM File ORDER BY fid ASC")
    for file in files:
      fileparts = db.GqlQuery("SELECT * FROM FilePart WHERE fid=%d" %file.fid)
      if file.parts == fileparts.count():
        self.response.out.write(u"创建时间: %s<br />地址: %s<br />文件名: %s<br />" %(cgi.escape((file.time + datetime.timedelta(hours=8) ).strftime("%Y-%m-%d %X")), file.url, file.filename))
        if file.parts == 1:
          self.response.out.write(u"<a href='/getfile?fid=%d&part=%d&single=true'>Download</a><br />" %(file.fid, 0))
        else:
          for part in range(file.parts):
            self.response.out.write(u"<a href='/getfile?fid=%d&part=%d'>Download: part%d</a><br />" %(file.fid, part, part))
        self.response.out.write(u"###ITEM END###<br /><br />")
        #self.response.headers['Content-Type'] = 'application/octet-stream'
        #for filepart in fileparts:
        #  self.response.out.write(filepart.bin)
        #if (file and file.bin):
        #    self.response.headers['Content-Type'] = 'application/octet-stream'
        #    self.response.out.write(file.bin)
        #else:
        #    self.response.headers['Content-Type'] = 'text/html'
        #    self.response.out.write(u"This File Not Found!")

def main():
  application = webapp.WSGIApplication([('/.*', MainHandler)],
                                       debug=True)
  util.run_wsgi_app(application)

if __name__ == '__main__':
  main()
