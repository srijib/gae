from google.appengine.ext import webapp
from google.appengine.ext.webapp import util

class MainPage(webapp.RequestHandler):
  def get(self):
    self.response.out.write(u"""该页不支持 GET""")
  def post(self):
    self.response.out.write(u"""
<html>
<head>
<title>下载歌曲</title>
<link type="text/css" rel="stylesheet" href="/static/main.css" />
</head>
<body>(请右键另存为,或者复制到下载工具,否则会失败!)<br/>""")
    url = self.request.get('url')
    self.response.out.write(u"<a href='%s'>%s</a>" %(url,url) )
    self.response.out.write(u"""
</body></html>""")
def main():
  application = webapp.WSGIApplication([('/.*', MainPage)],
                                       debug=True)
  util.run_wsgi_app(application)
if __name__ == '__main__':
  main()