#!/usr/bin/env python
# -*- coding: utf-8 -*-
import webapp2
from google.appengine.api import urlfetch
from google.appengine.api.urlfetch import DownloadError
from google.appengine.ext.webapp import template
from google.appengine.ext import db
from model import Task, Result
import time, datetime
def mod_task(task):
    timedelta = datetime.timedelta(hours = 8)
    task.detail_link = "/detail?key=%s" %task.key()
    task.test_link = "/work?key=%s" %task.key()
    #task.delete_link = "/delete?key=%s" %task.key()
    task.state = 'on' if task.enabled else 'off'
    task.toggle_link = "/toggle?key=%s" %task.key()
    task.toggle_link_str = 'disable it' if task.enabled else 'enable it'
    task.time += timedelta
    return task
def mod_result(result):
    timedelta = datetime.timedelta(hours = 8)
    result.time += timedelta
    return result
def redirect_to_referer(obj):
    url = obj.request.headers.get('Referer', '/list')
    obj.redirect(url)
class MainHandler(webapp2.RequestHandler):
    def get(self):
        template_values = {}
        self.response.out.write(template.render("template/index.tpl.html", template_values))
class TestListHandler(webapp2.RequestHandler):
    def get(self):
        tasks = Task.all().fetch(1000)
        timedelta = datetime.timedelta(hours = 8)
        for task in tasks:
            task = mod_task(task)
        template_values = {
            "tasks": tasks,
            }
        self.response.out.write(template.render("template/list.tpl.html", template_values))
class TestDetailHandler(webapp2.RequestHandler):
    def get(self):
        key = self.request.get("key")
        task = db.get(key)
        if not task:
            self.response.out.write("task key not exist")
            return
        # task found
        # start of time calc
        from_time = self.request.get("from")
        to_time = self.request.get("to")
        time_delta = datetime.timedelta(hours = 8)
        if from_time:
            try:
                from_time = datetime.datetime.strptime(from_time, "%Y.%m.%d") - time_delta
            except ValueError:
                pass
        if not from_time:
            from_time = datetime.datetime.now() - datetime.timedelta(hours = 24)
        if to_time:
            try:
                to_time = datetime.datetime.strptime(to_time, "%Y.%m.%d") - time_delta
            except:
                pass
        if not to_time:
            to_time = datetime.datetime.now()
        # end of time calc
        results = db.GqlQuery("SELECT * FROM Result WHERE task = :1 AND time >= :2 AND time <= :3 ORDER BY time DESC", task.key(), from_time, to_time)
        total = results.count()
        error = 0
        data_array = []
        results10 = results.fetch(10)
        for result in results10:
            result = mod_result(result)
        results = results.fetch(1000)
        for result in results:
            # print result.time
            result = mod_result(result)
            value = 1 if result.ok else 0
            data_array.append([time.mktime(result.time.timetuple()), value])
            if not result.ok: error += 1
        data_array.reverse()
        if total > 0:
            error_percent = error * 100.0 / total
        else:
            error_percent = 0.0
        task = mod_task(task)
        task.status_str = "error: %d, total: %d, error percent: %.2f%%" %(error, total, error_percent)
        chart_title = "Push Status (%s - %s)" %(str(from_time + time_delta), str(to_time + time_delta))
        limit = self.request.get('limit')
        try:
            limit = int(limit)
        except:
            limit = 10
        errors = db.GqlQuery("SELECT * FROM Result WHERE task = :1 AND ok = False AND time >= :2 AND time <= :3 ORDER BY time DESC LIMIT %d" %limit, task.key(), from_time, to_time)
        errors = errors.fetch(1000)
        for error in errors:
            error = mod_result(error)
        template_values = {
            "data_array": data_array,
            "chart_title": chart_title,
            "task": task,
            "limit": limit,
            "results": results10,
            "errors": errors,
            }
        self.response.out.write(template.render("template/detail.tpl.html", template_values))
class AddTestHandler(webapp2.RequestHandler):
    def get(self):
        template_values = {}
        self.response.out.write(template.render("template/add.tpl.html", template_values))
    def post(self):
        name = self.request.get("name")
        url = self.request.get("url")
        if (not name or not url):
            self.response.out.write("name and url required")
            return
        # name and url ok
        new_task = Task(name = name, url = url.strip())
        new_task.put()
        #self.response.out.write('<p>Task added OK</p><p><a href="/">back</a></p>')
        self.redirect("/list")
class DeleteTestHandler(webapp2.RequestHandler):
    def get(self):
        key = self.request.get("key")
        task = db.get(key)
        if not task:
            self.response.out.write("task key not exist")
            return
        # task found
        task.delete()
        # self.response.out.write('Task named "%s" deleted.' %task.name)
        redirect_to_referer(self)
    def post(self):
        self.response.out.write('Hello world!')
class ToggleTestHandler(webapp2.RequestHandler):
    def get(self):
        key = self.request.get("key")
        task = db.get(key)
        if not task:
            self.response.out.write("task key not exist")
            return
        # task found
        task.enabled = not task.enabled
        task.put()
        redirect_to_referer(self)
class OnceHandler(webapp2.RequestHandler):
    def get(self):
        template_values = {}
        self.response.out.write(template.render("template/once.tpl.html", template_values))
    def post(self):
        self.response.out.write("not impl")
class CronHandler(webapp2.RequestHandler):
    def get(self):
        from google.appengine.api import taskqueue
        tasks = Task.all().fetch(1000)
        for task in tasks:
            if task.enabled:
                taskqueue.add(url='/work', method="GET", params={"key": task.key()})
        self.response.out.write('Queued all tasks complete.')
class WorkHandler(webapp2.RequestHandler):
    def get(self):
        key = self.request.get("key")
        if not key:
            self.response.out.write('task key required')
            return
        # key ok
        task = db.get(key)
        if not task:
            self.response.out.write('task key not exist')
            return
        # task exist
        u_title = u"Toast测试"
        u_subtitle = u"时间:%s" %str(datetime.datetime.now()+datetime.timedelta(hours=8))
        toastMessage = "<?xml version=\"1.0\" encoding=\"utf-8\"?>" + \
            "<wp:Notification xmlns:wp=\"WPNotification\">" + \
               "<wp:Toast>" + \
                    "<wp:Text1>" + u_title.encode("utf-8") + "</wp:Text1>" + \
                    "<wp:Text2>" + u_subtitle.encode("utf-8") + "</wp:Text2>" + \
               "</wp:Toast> " + \
            "</wp:Notification>"
        request_headers = {
            "Content-Type": "text/xml",
            "X-WindowsPhone-Target": "toast",
            "X-NotificationClass": "2",
        }
        info = ""
        request_content = toastMessage
        response_content = ""
        response_headers = {}
        response_code = None
        subscription_status = ""
        deviceconnection_status = ""
        notification_status = ""
        ok = False
        try:
            response = urlfetch.fetch(url=task.url, headers=request_headers, payload=toastMessage, method="POST")
            response_content = response.content
            response_code = response.status_code
            response_headers = response.headers
            subscription_status = response_headers.get('x-subscriptionstatus', '')
            deviceconnection_status = response_headers.get('x-deviceconnectionstatus', '')
            notification_status = response_headers.get('x-notificationstatus', '')
            if subscription_status or deviceconnection_status or notification_status:
                info = "Result: {subscriptionstatus: %s, deviceconnectionstatus: %s, notificationstatus: %s}" %(subscription_status, deviceconnection_status, notification_status)
            else:
                info = "Result: Error"
            if subscription_status == "Active" and deviceconnection_status == "Connected" and notification_status == "Received" : ok = True
        except DownloadError as e:
            info = "".join(e.args)
        self.response.out.write(info)
        result = Result(
            task = task,
            type = Result.Toast,
            
            request_headers = str(request_headers),
            request_content = request_content.decode("utf-8"),
            
            response_headers = str(response_headers),
            response_content = response_content.decode("utf-8"),
            response_code = response_code,
            
            subscription_status = subscription_status,
            deviceconnection_status = deviceconnection_status,
            notification_status = notification_status,
            
            ok = ok,
            info = info,
        )
        result.put()
        self.response.out.write('<br><br>End Of This Page.')

app = webapp2.WSGIApplication(
    [
        ('/', MainHandler),
        ('/list', TestListHandler),
        ('/detail', TestDetailHandler),
        ('/add', AddTestHandler),
        ('/delete', DeleteTestHandler),
        ('/toggle', ToggleTestHandler),
        ('/once', OnceHandler),
        ('/cron', CronHandler),
        ('/work', WorkHandler),
    ], debug=True)
