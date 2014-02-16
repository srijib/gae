from google.appengine.ext import webapp
from google.appengine.ext.webapp import util
from google.appengine.ext import db
from google.appengine.api import urlfetch
from google.appengine.api.labs import taskqueue
import urllib,cgi,re

class FID(db.Model):
  total = db.IntegerProperty()

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

def getFID():
    fids = db.GqlQuery("SELECT * FROM FID")
    if fids.count() == 0:
      fid = FID(total=0)
      fid_now = fid.total
      fid.put()
      return fid_now
    else:
      fid = fids.get()
      fid.total+=1
      fid_now = fid.total
      fid.put()
      return fid_now

class MainHandler(webapp.RequestHandler):
  def post(self):
    url = self.request.get("url")
    filename = self.request.get("filename")
    filesize = None
    try:
      info = urlfetch.Fetch(url = url, headers={'Range':'bytes=0-5'})
      try:
        filesize = int(info.headers['x-amz-meta-s3fox-filesize'])
      except:
        try:
          size_strs = re.split(r"/", info.headers['Content-Range'])
          filesize = int(size_strs[-1])
        except:
          try:
            filesize = int(info.headers['Content-Length'])
          except:
            pass
    except:
      self.response.out.write(u'获取文件信息失败')
    if filesize:
      #开始创建文件信息
      parts = filesize/1024000 + 1
      fid = getFID()
      if not filename:
        try:
          filename = re.split(r"/", url)[-1]
        except:
          pass
      file = File(url=url, fid=fid, filesize=filesize, parts=parts, filename = filename)
      file.put()
      #开始下载
      #try:
      for part in range(parts):
        start = part*1024000
        end = (part+1)*1024000-1
        taskqueue.add( url='/fetch',
                       method='GET',
                       params = {'url': url, 'part': str(part), 'start': str(start), 'end': str(end), 'fid':fid}
                      )
        #data = urlfetch.Fetch(url = url, headers={'Range':"bytes=%d-%d" %(start, end)})
        #part = FilePart(fid=fid, part=part, url=url, filename=filename)
        #part.bin = db.Blob(data.content)
        #part.put()
      self.response.out.write(u'任务已添加! 文件大小: %s 字节' %filesize)
      #except:
      #  self.response.out.write(u'下载时错误')
    else:
      pass
      #self.response.out.write(u'获取文件大小失败')
def main():
  application = webapp.WSGIApplication([('/.*', MainHandler)],
                                       debug=True)
  util.run_wsgi_app(application)

if __name__ == '__main__':
  main()
