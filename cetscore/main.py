from google.appengine.ext import webapp
from google.appengine.ext.webapp import util
from google.appengine.api import urlfetch
import urllib
def print_head(self):
  self.response.out.write(u'<h1>四六级成绩批量查询</h1>')
  self.response.out.write(u'<h3>方便忘记准考证号和不想等待倒计时的人使用</h3>')
  self.response.out.write(u'<br />')
def print_end(self):
  self.response.out.write(u"<br />By eggfly(SJTU) 2010.3.3")

class MainHandler(webapp.RequestHandler):

  def get(self):
    print_head(self)
    self.response.out.write(u"""
      <form action='/' method="post">准考证号:<input name="id" type="text" maxlength="15" /><input type="submit" value="查询附近同学成绩" />
      </form>""")
    
    print_end(self)
  def post(self):
    print_head(self)
    ####start
    persons = 16
    id = int(self.request.get("id")) - persons/2
    url = 'http://cet.99sushe.com/getscore.html'
    ##
    self.response.out.write(u"听力,阅读,综合,写作,成绩总分,学校,姓名<br />")
    for i in range(persons):
      data = urllib.urlencode(
        {
          'id': str(id+i),
          'vc': 'novcversion'
        })
      result = urlfetch.fetch(
        url = url,
        payload = data,
        headers = {
          'Referer':'http://cet.99sushe.com/',
          'Content-Type': 'application/x-www-form-urlencoded;charset=gb2312'},
        method=urlfetch.POST)
      self.response.out.write(unicode(result.content,"GB18030"))
      self.response.out.write(u"<br />")
    #end for
    self.response.out.write(u"<br /><a href='/'>返回</a>")
    print_end(self)
def main():
  application = webapp.WSGIApplication([('/.*', MainHandler)],
                                       debug=True)
  util.run_wsgi_app(application)


if __name__ == '__main__':
  main()
