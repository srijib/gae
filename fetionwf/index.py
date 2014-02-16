from google.appengine.ext import webapp
from google.appengine.ext.webapp import util
from google.appengine.ext import db
from google.appengine.api import urlfetch
import re,cgi

class MainPage(webapp.RequestHandler):
  def get(self):
    self.response.out.write(u"""
      <html>
      <head>
        <script src="/static/jquery-1.4.min.js"></script>
        <meta name="google-site-verification" content="M02NO8cMYuXaJUaz6t9tHVWhR8JwCDs--9Sxn6BXvJ8" />
        <title>飞信天气预报</title>
        <link type="text/css" rel="stylesheet" href="/static/main.css" /> 
        </head>
      <body>
        <table width="1024" height="635" align="center" background="/static/weather.gif">
        <tr><td>
        <table align="center" Bgcolor="#000000"><tr><td>
        <div align="center" valign="middle">
        <!--<h1>飞信天气预报</h1>-->
        <!--<h3>☆支持定时发送☆ <a href="/task">查看任务列表</a></h3>-->
        <script>
        function getredirect(v) {
          if (v=='') v = 123;
          self.frames['preview'].location.href = '/do?city='+v;
        }
        </script>
        <table border="0" cellpadding="0" cellspacing="0" bordercolor="#CCCCCC" Bgcolor="#000000">
        <td colspan = "3" valign="middle" align="center" ><a href="http://fetionwf.appspot.com">http://fetionwf.appspot.com</a></td></tr>
        <tr><td><p></p></td></tr><tr><td>
        <table border="0" height="190" border="0" cellpadding="0" cellspacing="0" >
        <tr>
        <td align="right" valign="middle">选择城市:</td>
        <td>
        <form name="input" action="do" method="get">
        <select id="obSelect" name="city" onchange="getredirect(this.value)" style="width:122px;height:18px">
        <option value="1">香港</option><option value="2">澳门</option>
        <option value="280">台北</option>
        <option value="125">北京</option><option value="252">上海</option>
        <option selected value="127">天津</option><option value="212">重庆</option>
        <option value="115">沈阳</option><option value="103">长春</option>
        <option value="17">哈尔滨</option><option value="244">南京</option>
        <option value="211">武汉</option><option value="292">广州</option>
        <option value="140">济南</option><option value="255">杭州</option>
        <option value="166">成都</option><option value="296">深圳</option>
        <option value="287">厦门</option><option value="28">乌鲁木齐</option>
        <option value="56">西宁</option><option value="57">兰州</option>
        <option value="69">呼和浩特</option><option value="78">银川</option>
        <option value="82">石家庄</option><option value="84">太原</option>
        <option value="150">拉萨</option><option value="179">昆明</option>
        <option value="186">西安</option><option value="189">郑州</option>
        <option value="218">长沙</option><option value="227">贵阳</option>
        <option value="232">桂林</option><option value="248">合肥</option>
        <option value="264">南昌</option><option value="276">福州</option>
        <option value="295">南宁</option><option value="303">海口</option> 
        </select>
        </td>
        <td rowspan = 4 valign="middle" align="center" ><input style="width:60px;height:50px;" type="submit" value="发送!"></td>
        </tr>
        <tr><td align="right" valign="middle">发送手机:</td><td><input onkeyup="value=this.value.replace(/\D+/g,'')" type="text" name="from" style="width:122px;height:18px;ime-mode:Disabled" maxlength="11" /></td></tr>
        <tr><td align="right" valign="middle">飞信密码:</td><td><input type="password" name="password" style="width:122px;height:18px" maxlength="30" /><td></tr>
        <tr><td align="right" valign="middle">接收手机:</td><td><input onkeyup="value=this.value.replace(/\D+/g,'')" type="text" name="to" style="width:122px;height:18px;ime-mode:Disabled" maxlength="11" /></td></tr>
        <tr><td colspan='3' align="left" valign="middle">『网站不会记录飞信密码,发送时飞信会掉线..』</td></tr>
        <tr><td colspan='3' align="left" valign="middle">发送内容预览: <a href='#' onclick='$("#preview").toggle("slow")'>显示/隐藏</a></td></tr>
        <tr id='preview_tr'><td colspan='3' align="left" valign="middle">
        <iframe  name='preview' id='preview' width='250' height='75' align='center' marginwidth='0' marginheight='0' hspace='0' vspace='0' frameborder='0' scrolling='no' src='/do' ></iframe>
        </td></tr>
        <tr><td colspan='3' align="left" valign="middle">您的信息: <a href='#' onclick='$("#info").toggle("slow")'>显示/隐藏</a></td></tr>
        
        <tr><td id='info' colspan='3' valign="middle">""")
    
    self.response.out.write(u"IP地址:" + self.request.remote_addr.encode('utf-8'))
    try:
      ip_url = "http://www.ip.cn/getip.php?action=queryip&ip_url=" + self.request.remote_addr.encode('utf-8')
      ip_result = urlfetch.fetch(ip_url)
      if ip_result.status_code == 200:
        result_content = unicode( ip_result.content, "GBK")
        addr = (re.split( ur"来自：", result_content ))[-1]
        self.response.out.write(u"<br>地址: " + addr)
    except:
      pass
    UserAgent = self.request.headers['User-Agent']
    #self.response.out.write(u"<br>User Agent:<br>" + UserAgent.encode('utf-8'))
    browser = re.search(r"(?:Firefox|Opera|Safari|Chrome|MSIE|UP\.Browser|Opera Mobi|UCWEB|GoBrowser)[\/: ]?([\d.]+)?", UserAgent)
    if browser:
      self.response.out.write(u"<br>浏览器: " + browser.group())
    else :
      pass
      #self.response.out.write(u"<br>浏览器: 未知")
    
    os=re.search(r"(?:Windows NT|Windows|SymbianOS|Series60|S60|SymbOS|Linux|Mac OS|MacOS|Mac|Nokia|NOKIA|Unix)[\/: ]?([\d.]+)?", UserAgent)
    if os:
      if re.search(r"Windows NT 6.1",UserAgent):
        self.response.out.write(u"<br>操作系统: Windows 7")
      elif re.search(r"Windows NT 6.0",UserAgent):
        self.response.out.write(u"<br>操作系统: Windows Vista")
      elif re.search(r"Windows NT 5.2",UserAgent):
        self.response.out.write(u"<br>操作系统: Windows 2003")
      elif re.search(r"Windows NT 5.1",UserAgent):
        self.response.out.write(u"<br>操作系统: Windows XP")
      elif re.search(r"Windows NT 5.0",UserAgent):
        self.response.out.write(u"<br>操作系统: Windows 2000")
      elif re.search(r"Windows 9",UserAgent) or re.search(r"Windows 4",UserAgent):
        self.response.out.write(u"<br>操作系统: Windows 9x")
      elif re.search(r"Ubuntu",UserAgent):
        self.response.out.write(u"<br>操作系统: Ubuntu Linux")
      elif re.search(r"Mac",UserAgent) or re.search(r"MacOS",UserAgent):
        self.response.out.write(u"<br>操作系统: Mac OS")
      else:
        self.response.out.write(u"<br>操作系统: " + os.group())
    else:
      pass
      #self.response.out.write(u"<br>操作系统: 未知")
    self.response.out.write(u"""</td></tr>
        <tr><td colspan = "2" valign="middle">飞信天气预报 v0.2.4 by eggfly </td> <td align="left" valign="middle"><iframe name='pageview' id='pageview' width='80' height='15' align='center' marginwidth='0' marginheight='0' hspace='0' vspace='0' frameborder='0' scrolling='no' src='/statistic'></iframe></td></tr>
        
        <tr>
        <td colspan = "3" valign="middle" align="center" ><a href="/static/reg.html">每日定时发送~New!</a> <a href="/task">当前任务列表</a> <a href="/static/help.html">帮助</a></td></tr>
        <tr>
        <td colspan = "3" valign="middle" align="center" ><a href="/static/changelog.html">更新日志</a> <a href="/message">留言板</a> <a href="http://renrenfarm.appspot.com">☆人人开心农场助手~☆</a></td></tr>
        </form>
        </table>
        </td></tr>
        </table>
        </div>
        </td></tr>
        </table>
        </td></tr>
        </table>
      </body>
    </html>""")

def main():
  application = webapp.WSGIApplication([('/.*', MainPage)],
                                       debug=True)
  util.run_wsgi_app(application)
if __name__ == '__main__':
  main()