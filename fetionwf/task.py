import cgi
from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext import db
from google.appengine.api import urlfetch
import datetime,time
class TaskCount(db.Model):
  total = db.IntegerProperty()
class Task(db.Model):
  id = db.IntegerProperty()
  user = db.StringProperty()
  login_passwd = db.StringProperty()
  city = db.StringProperty()
  from_num = db.StringProperty()
  fetion_passwd = db.StringProperty()
  to_num = db.StringProperty()
  time = db.DateTimeProperty()
  add_time = db.DateTimeProperty(auto_now_add=True)

class MainPage(webapp.RequestHandler):
  def get(self):
    self.response.out.write(u"""
      <html>
      <head>
      <title>Task list</title>
      <link type="text/css" rel="stylesheet" href="/static/main.css" /> 
      </head>
      <body>
      <h1>任务列表 (按时间顺序)</h1>""")
    tasks = db.GqlQuery("SELECT * FROM Task ORDER BY time ASC")
    for task in tasks:
      self.response.out.write(u'<b>%s</b> 的任务: ( Task ID: %d )' % (cgi.escape(task.user),task.id))
      self.response.out.write(u'&nbsp;&nbsp;<a href=\'/task/delete?id=%d\'>删除此任务</a>' % task.id)
      self.response.out.write(u'<blockquote>From:&nbsp;&nbsp;%s&nbsp;&nbsp;To:&nbsp;&nbsp;%s</blockquote>' % (cgi.escape(task.from_num),cgi.escape(task.to_num)))
      self.response.out.write(u'<blockquote>计划时间:%s&nbsp;&nbsp;现在时间:%s</blockquote>' %(
                              cgi.escape((task.time + datetime.timedelta(hours=8) ).strftime("%Y-%m-%d %X")), cgi.escape(time.strftime('%Y-%m-%d %X', time.gmtime( time.time() + 8*60*60) ))))
      if datetime.datetime.now() - datetime.timedelta(days=1) <= task.time < datetime.datetime.now():
        #self.response.out.write(u'<blockquote>执行任务成功!</blockquote>')
        #deal with it
        url = 'http://fetionwf.appspot.com/do?city=' + task.city + '&from=' + task.from_num + '&password=' + task.fetion_passwd.replace(" ","%20") + '&to=' + task.to_num
        #self.response.out.write(url)
        result = urlfetch.fetch(url)
        if result.status_code == 200:
          self.response.out.write(u'<blockquote>执行任务成功!</blockquote>')
        #end
        task.time = task.time + datetime.timedelta(days=1)
        task.put()
    self.response.out.write(u"""
        <a href = "/static/reg.html">返回</a>  <a href="/">返回主页</a>
        </body>
      </html>""")
class Reg(webapp.RequestHandler):
  def post(self):
    total = 0
    task = Task()
    taskcounts = db.GqlQuery("SELECT * FROM TaskCount")
    if taskcounts.count() != 0 :
      for taskcount in taskcounts:
        taskcount.total += 1
        total = taskcount.total
        taskcount.put()
    else:
      taskcount = TaskCount()
      taskcount.total = 0
      total = taskcount.total
      taskcount.put()
    task.id = total
    task.user = self.request.get('user')
    task.login_passwd = self.request.get('login_passwd')
    task.city = self.request.get('city')
    task.from_num = self.request.get('from_num')
    task.fetion_passwd = self.request.get('fetion_passwd')
    task.to_num = self.request.get('to_num')
    
    task.time = datetime.datetime(time.gmtime()[0],time.gmtime()[1],time.gmtime()[2], int(self.request.get('hour')), int(self.request.get('minute')) ) - datetime.timedelta(hours=8)
    if task.time <= datetime.datetime.now():
      task.time += datetime.timedelta(days=1)
    if task.login_passwd and task.user and task.city and task.from_num and task.fetion_passwd and task.to_num :
      task.put()
    self.redirect('/task')

application = webapp.WSGIApplication(
                                     [('/task', MainPage),
                                      ('/task/reg', Reg)],
                                     debug=True)

def main():
  run_wsgi_app(application)

if __name__ == "__main__":
  main()
