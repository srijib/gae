#!/usr/bin/env python
# -*- coding: utf-8 -*-
from google.appengine.ext import webapp
from google.appengine.ext.webapp import util
from google.appengine.ext.webapp import template
from models import *
from lib import MyHandler, approximate_size
class HomeHandler(MyHandler):
    def get(self):
        self.response.out.write(u"""<h1><a href="/upload">集群高速网盘</a></h1>""")
class DownloadHandler(MyHandler):
    def get(self):
        r_path = self.request.path
        key = r_path.split("/")[-1]
        if key == "" or key == "dl":
            self.response.out.write("No key given.")
            return
        file = db.get(db.Key(key))
        if not file:
            self.response.out.write("File not Found. Maybe it has been removed.")
            return
        file.downloads += 1
        file.put()
        self.redirect(file.url)
class UploadHandler(MyHandler):
    def get(self):
        template_file = {}
        disk = Disk.all().order("used").get()
        if not disk:
            self.response.out.write(u"""系统集群尚未初始化,请联系管理员.""")
            self.response.set_status(400)
            return
        template_file["upload_url"] = disk.host + "/upload"
        template_file["disk_key"] = disk.key()
        files = FileRecord.all().order("-time").fetch(1000)
        for f in files:
            f.size_str = approximate_size(f.size)
            if f.filename.endswith(".pdf"):
                f.preview = u"""<a href="%s/pdfpreview?key=%s&startpage=1&endpage=10">预览</a>""" %(f.location.host, f.url.split("key=")[-1])
            else:
                f.preview = ""
        template_file["files"] = files
        self.render("views/upload.html", template_file)
class NotifyHandler(MyHandler):
    def get(self):
        self.response.out.write(u"""Notifier: Method not supported.""")
        self.response.set_status(405)
    def post(self):
        size = self.request.get("size")
        filename = self.request.get("filename")
        tag = self.request.get("tag")
        url = self.request.get("url")
        disk_key = self.request.get("disk_key")
        if not(size and filename and url and disk_key): #
            self.response.out.write(u"""Error: Notifier need these: size, filename, url, tag(or empty) and disk_key.""")
            self.response.set_status(400)
            return
        disk = Disk.get(db.Key(disk_key))
        size = int(size)
        disk.used += size
        disk.put()
        new_file = FileRecord(filename = filename, url = url, size = size, tag = tag, location = disk)
        new_file.put()
        self.response.out.write(u"""Notified a file OK.""")
class StatusHandler(MyHandler):
    def get(self):
        template_file = {}
        disks = Disk.all().fetch(10000)
        total = Disk.total
        total_used = total_total = 0
        for d in disks:
            total_used += d.used
            total_total += total
            d.free_str = approximate_size(total - d.used)
            d.used_str = approximate_size(d.used)
            d.percent_str = "%.2f%%" %(100.0 * d.used / total)
        template_file["disks"] = disks
        template_file["used"] = approximate_size(total_used)
        template_file["total"] = approximate_size(total_total)
        template_file["free"] = approximate_size(total_total - total_used)
        template_file["percent"] = "%.2f%%" %(100.0 * total_used / total_total)
        self.render("views/status.html", template_file)
def main():
    application = webapp.WSGIApplication([('/', HomeHandler), ('/upload', UploadHandler), ('/notify', NotifyHandler), ('/dl.*', DownloadHandler), ('/status', StatusHandler),],
                                         debug=True)
    util.run_wsgi_app(application)

if __name__ == '__main__':
    main()
