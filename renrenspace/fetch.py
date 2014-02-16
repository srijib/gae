from google.appengine.ext import webapp
from google.appengine.ext.webapp import util
from google.appengine.api import urlfetch
from google.appengine.ext import db

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

class MainPage(webapp.RequestHandler):
  def get(self):
    url = self.request.get('url')
    part = self.request.get('part')
    start = self.request.get('start')
    end = self.request.get('end')
    fid = self.request.get('fid')
    filename = db.GqlQuery("SELECT * FROM File WHERE fid=%s" %fid).get().filename
    #这里容易出错 错了更好
    if url and start and end and fid and filename:
      data = urlfetch.fetch( url = url,
                               headers={'Range':"bytes=%s-%s" %(start, end)}
                              )
      
      fileparts = db.GqlQuery("SELECT * FROM FilePart WHERE fid=%s AND part=%s" %(fid, part))
      if fileparts.count()==0:
        filepart = FilePart(fid=int(fid), part=int(part), url=url, filename=filename)
      else:
        filepart = fileparts.get()
      filepart.bin = db.Blob(data.content)
      filepart.put()
      self.response.set_status(data.status_code)

  def post(self):
    self.response.out.write(u"""该页不支持POST""")
def main():
  application = webapp.WSGIApplication([('/.*', MainPage)],
                                       debug=True)
  util.run_wsgi_app(application)
if __name__ == '__main__':
  main()