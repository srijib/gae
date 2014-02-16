#!/usr/bin/python
# -*- coding: utf-8 -*-
from google.appengine.ext import webapp
from google.appengine.ext.webapp import util
from google.appengine.api import urlfetch
import re
import time
class MainHandler(webapp.RequestHandler):
  def get(self):
    #url1= "http://m.weather.com.cn/m/pn2/weather.htm?id=101030100T"
    #url1= "http://weather.news.qq.com/inc/ss127.htm"
    #url1 = "http://news.sina.com.cn/iframe/weather/120100.html"
    #url1 = "http://www.nmc.gov.cn/publish/forecast/ATJ/tianjin.html"
    #url1 = 'http://php.weather.sina.com.cn/search.php?city=%CC%EC%BD%F2&dpc=1'
    if self.request.get('city').encode('utf-8') != '':
      url1 = 'http://weather.news.qq.com/inc/07_dc' + self.request.get('city').encode('utf-8') +'.htm'
    else :
      url1 = 'http://weather.news.qq.com/inc/07_dc127.htm'
    result1 = urlfetch.fetch(url1)
    if result1.status_code == 200:
      content = unicode( result1.content, "GBK")
      doc = re.sub(r'<(S*?)[^>]*>.*?|<.*? /> ','', content ).strip()
      find_str = u'气象信息由中央气象台提供'
      #print doc.replace(" ",'').replace("&nbsp;",'').replace('&#160;','').replace(u'·','').replace(u'：',':').replace(" \n",'').encode("utf-8")
      result = re.split(find_str,doc)
      #print result[3].encode("utf-8")
      wanted = result[1].replace(" ",'').replace("&nbsp;",'').replace('&#160;','').replace(u'·','').replace(u'：',':')
      city = re.split(u"&#160;", result[0])
      city_str = city[1]
      city_str = city_str.replace("\n","")
      #print city_str.encode("utf-8")
      tj = "##".join(wanted.split())
      #print "\n".join(tj.split('##')).encode("utf-8")
      #data = "".join(tj.split('##'))
      #date = re.findall(u"(\d\d?日星期.)",data)
      #temp = re.findall(u"(高温-?\d+℃低温-?\d+℃)",data)
      #weather = re.findall(u"(白天##夜晚..?.?##..?.?##)",tj)
      #wind = re.findall(u"(℃##..?风..?.?级##)",tj)
      #data = re.findall(u"(\d\d?日星期.##白天##夜晚##..?.?##..?.?##高温-?\d\d?℃#?#?低温-?\d\d?℃##..?风..?.?.?级##.?.?风?.?.?.?.?级?)", tj)
      
      #腾讯网预报正则匹配
      now = re.findall(u"(当前天气##.+?-?\d+℃～-?\d+℃##.+?:.+?##.+?:..?.?.?##.+?:..?.?.?##)", tj)
      data = re.findall(u"(\d+-\d+-\d+##.+?#?#?-?\d+℃～-?\d+℃##..?.?.?.?.?.?.?.?##)", tj)
      #print now[0].encode('utf-8')
      data2 = data[1].split("##")
      now2 = now[0].split("##")
      #for i in now2:
      #  print i.encode('utf-8')
      #for i in data2:
      #  print i.encode('utf-8')
      str = "%20".join(now2) + u"24小时预报:" + "%20".join(data2)
      str = str.replace(u" ",u"%20").replace(u"～",u"~")
      #self.response.out.write(str.encode("utf-8"))
      #print date[1].encode('utf-8')
      #print temp[0].encode('utf-8')
      #print weather[0].encode('utf-8')
      #print wind[0].encode('utf-8')
      #doSomethingWithResult(result.content)
      #finalstr = "%20天气预报:" + date[0].encode('utf-8') + '夜晚:' + (weather[0].split('##'))[-1].encode('utf-8') + (wind[0].split('##'))[1].encode('utf-8') +temp[0].encode('utf-8') + '; ' + date[1].encode('utf-8') + '白天:' + (weather[0].split('##'))[-2].encode('utf-8') + (wind[1].split('##'))[1].encode('utf-8') + temp[1].encode('utf-8') + "%20(天气预报每日发送,若有程序错误请通知我,我会及时更正,谢谢!)"
      finalstr = "%20" + city_str.encode("utf-8") +"%20" + str.encode('utf-8')
      #self.response.out.write('<iframe width="606" height="350" align="center" marginwidth="0" marginheight="0" hspace="0" vspace="0" frameborder="0" scrolling="no" src="http://weather.news.qq.com/inc/07_dc127.htm"></iframe>')
      self.response.out.write("""
<style type="text/css"> 
<!--
body {
	background-color: #000000;
	background-image: url();
}
body,td,th {
	font-size: 12px;
	color: #FFFFFF;
}
.inputcss{
	background: #FFFFFF;
    border-bottom: #000000 1px solid;
    border-left: #000000 1px solid;
    border-right: #000000 1px solid;
    border-top: #000000 1px solid;
    color: #000000;
    cursor: text;
    font-size: 9pt;
    padding: 1px;
}
-->
</style>
        """)
      self.response.out.write("<br>" + finalstr.replace('%20',' '))
      #self.response.out.write("<br>" + finalstr)
      if self.request.get('from').encode('utf-8') != '' and self.request.get('password').encode('utf-8') != '' and self.request.get('to').encode('utf-8') != '':
        url2="https://sms.api.bz/fetion.php?username=" + self.request.get('from').encode('utf-8') +"&password=" + self.request.get('password').encode('utf-8') +"&sendto=" + self.request.get('to').encode('utf-8') +"&message=" + finalstr
        result2 = urlfetch.fetch(url2)
        if result2.status_code == 200:
          #print result2.content
          #doSomethingWithResult(result.content)
          self.response.out.write('<br>' + self.request.get('to').encode('utf-8') + ': Sent OK! ')
        else:
          self.response.out.write('<br>' + self.request.get('to').encode('utf-8') + ': Failed. ')
        self.response.out.write(unicode( result2.content, "utf-8").encode('utf-8'))
      else:
        if self.request.get('num').encode('utf-8') != '':
          SendList = []
          SendList.append(self.request.get('num').encode('utf-8'))
          self.response.out.write('<br>Manual target: ' + self.request.get('num').encode('utf-8'))
          
        else:
          SendList = [#"13920510408",#老婆
                      #"13682185616",#大嘴
                      #"15832876867",#姐姐
                      #"13820254193",#爸爸
                      #"15828514324",#孙佳维
                      
                      #"13888888888",#empty
                      #"13888888888",#empty
                      #"13888888888",#empty
                      #"13888888888",#empty
                      
                      #"13821254203"#自己
                      ]
        for i in SendList:
          url2="https://sms.api.bz/fetion.php?username=13821254203&password=snowmanshan0913&sendto=" + i +"&message=" + finalstr
          #url2="http://fetion.xinghuo.org.ru/restlet/fetion/13821254203/snowmanshan0913/" + i + "/" + finalstr
          result2 = urlfetch.fetch(url2)
          if result2.status_code == 200:
            #print result2.content
            #doSomethingWithResult(result.content)
            self.response.out.write('<br>' + i + ': Sent OK! ')
          else:
            self.response.out.write('<br>' + i + ': Failed. ')
            
          self.response.out.write(unicode( result2.content, "utf-8").encode('utf-8'))
          #time.sleep(1)
def main():
  application = webapp.WSGIApplication([('/do', MainHandler)],
                                       debug=True)
  util.run_wsgi_app(application)

if __name__ == '__main__':
  main()