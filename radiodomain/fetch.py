from google.appengine.ext import webapp
from google.appengine.ext.webapp import util
from google.appengine.api import urlfetch

class MainPage(webapp.RequestHandler):
  def get(self):
    verify_url = 'http://douban.fm/j/mine/playlist?uid=37249042'
    result = urlfetch.fetch(
      url=verify_url,
      headers={
                'Host': 'douban.fm',
                'Connection': 'keep-alive',
                'Cache-Control': 'max-age=0',
                'Accept': 'application/xml,application/xhtml+xml,text/html;q=0.9,text/plain;q=0.8,image/png,*/*;q=0.5',
                'Accept-Encoding': 'gzip,deflate,sdch',
                'Accept-Language': 'zh-CN,zh;q=0.8',
                'Accept-Charset': 'GBK,utf-8;q=0.7,*;q=0.3',
                'Cookie': 'rdat="1269068373"; __utmz=58778424.1268980546.2.2.utmcsr=music.douban.com|utmccn=(referral)|utmcmd=referral|utmcct=/; ac="1269068158"; ck="YQ4Q"; dbcl2="37249042:oeCCZsD4cqk"; bid="wy5342WKd04"; f=wrapper; __utma=58778424.786668245.1268976831.1269000443.1269068163.5; __utmc=58778424; __utmv=58778424.3724; __utmb=58778424.20.10.1269068163'
             },
      method=urlfetch.GET,
      follow_redirects = False
    )
    self.response.set_status(result.status_code)
    self.response.out.write(result.content)
  def post(self):
    self.response.out.write(u"""该页不支持POST""")
def main():
  application = webapp.WSGIApplication([('/.*', MainPage)],
                                       debug=True)
  util.run_wsgi_app(application)
if __name__ == '__main__':
  main()