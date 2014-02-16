from google.appengine.ext import webapp
from google.appengine.ext.webapp import util
from google.appengine.ext import db
from google.appengine.api import urlfetch
import re

class MainHandler(webapp.RequestHandler):
  def get(self):
    self.response.out.write(u"您的IP地址:" + self.request.remote_addr.encode('utf-8'))
    try:
      ip_url = "http://www.ip.cn/getip.php?action=queryip&ip_url=" + self.request.remote_addr.encode('utf-8')
      ip_result = urlfetch.fetch(ip_url)
      if ip_result.status_code == 200:
        result_content = unicode( ip_result.content, "GBK")
        addr = (re.split( ur"来自：", result_content ))[-1]
        self.response.out.write(u"(" + addr + u")")
    except:
      pass
    UserAgent = self.request.headers['User-Agent']
    self.response.out.write(u"<br>您的User Agent:<br>" + UserAgent.encode('utf-8'))
    browser = re.search(r"(?:Firefox|Opera|Safari|Chrome|MSIE|UP\.Browser|Opera Mobi|UCWEB)[\/: ]?([\d.]+)?", UserAgent)
    if browser:
      self.response.out.write(u"<br>您的浏览器: " + browser.group())
    else :
      pass
      #self.response.out.write(u"<br>您的浏览器: 未知")
    
    os=re.search(r"(?:Windows NT|Windows|SymbianOS|Series60|S60|SymbOS|Linux|Mac OS|MacOS|Mac|Nokia|NOKIA|Unix)[\/: ]?([\d.]+)?", UserAgent)
    if os:
      if re.search(r"Windows NT 6.1",UserAgent):
        self.response.out.write(u"<br>您的操作系统: Windows 7")
      elif re.search(r"Windows NT 6.0",UserAgent):
        self.response.out.write(u"<br>您的操作系统: Windows Vista")
      elif re.search(r"Windows NT 5.2",UserAgent):
        self.response.out.write(u"<br>您的操作系统: Windows 2003")
      elif re.search(r"Windows NT 5.1",UserAgent):
        self.response.out.write(u"<br>您的操作系统: Windows XP")
      elif re.search(r"Windows NT 5.0",UserAgent):
        self.response.out.write(u"<br>您的操作系统: Windows 2000")
      elif re.search(r"Windows 9",UserAgent) or re.search(r"Windows 4",UserAgent):
        self.response.out.write(u"<br>您的操作系统: Windows 9x")
      elif re.search(r"Ubuntu",UserAgent):
        self.response.out.write(u"<br>您的操作系统: Ubuntu Linux")
      elif re.search(r"Mac",UserAgent) or re.search(r"MacOS",UserAgent):
        self.response.out.write(u"<br>您的操作系统: Mac OS")
      else:
        self.response.out.write(u"<br>您的操作系统: " + os.group())
    else:
      pass
      #self.response.out.write(u"<br>您的操作系统: 未知")
def main():
  application = webapp.WSGIApplication([('/', MainHandler)],
                                       debug=True)
  util.run_wsgi_app(application)
if __name__ == '__main__':
  main()
