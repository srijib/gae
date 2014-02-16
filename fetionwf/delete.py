import cgi
from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext import db
from google.appengine.api import urlfetch
import datetime,time
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
      <title>Delete task</title>
      <link type="text/css" rel="stylesheet" href="/static/main.css" /> 
      </head>
      <body><h1>删除任务</h1>""")
    if self.request.get('id')!='' and self.request.get('password')!='':
      tasks = db.GqlQuery('SELECT * FROM Task WHERE id=%s' % self.request.get('id'))
      task = tasks.get()
      if self.request.get('password') == task.login_passwd:
        task.delete()
        self.response.out.write(u"""<br>删除成功!<br><a href='/task'>返回任务列表</a>""")
      else:
        self.response.out.write(u"""<br>密码错误,请后退重试.<br><a href='/task'>返回任务列表</a>""")
    else:
      self.response.out.write(u"""
        <form name="delete" action="/task/delete" method="post">""")
      self.response.out.write(u"""ID号:<input onkeyup="value=this.value.replace(/\D+/g,'')" type="text" name="id" style="width:96px;height:18px;ime-mode:Disabled" value='""")
      self.response.out.write(u'%s' % self.request.get('id'))
      self.response.out.write(u"""'></input>""")
      self.response.out.write(u"""<br>密码:<input type="password" name="password" style="width:96px;height:18px" maxlength="30"></input>""")
      self.response.out.write(u"""<br><input style="width:120px;height:24px" type="submit" value="删除">""")
    
    self.response.out.write("""
        </body>
        </html>""")
  def post(self):
    self.response.out.write(u"""
      <html>
      <head>
      <title>Delete task</title>
      <link type="text/css" rel="stylesheet" href="/static/main.css" /> 
      </head>
      <body><h1>删除任务</h1>""")
    if self.request.get('id')!='' and self.request.get('password')!='':
      tasks = db.GqlQuery('SELECT * FROM Task WHERE id=%s' % self.request.get('id'))
      task = tasks.get()
      if self.request.get('password') == task.login_passwd:
        task.delete()
        self.response.out.write(u"""<br>删除成功!<br><a href='/task'>返回任务列表</a>""")
      else:
        self.response.out.write(u"""<br>密码错误,请后退重试.<br><a href='/task'>返回任务列表</a>""")
    
    self.response.out.write("""
        </body>
        </html>""")

application = webapp.WSGIApplication(
                                     [('/task/delete', MainPage)],
                                     debug=True)

def main():
  run_wsgi_app(application)

if __name__ == "__main__":
  main()
