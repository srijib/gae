#!/usr/bin/env python
# -*- coding: utf-8 -*-
from google.appengine.ext import webapp
from google.appengine.ext.webapp import util
from models import *
from lib import MyHandler
import ADDRESS

class MainHandler(MyHandler):
    def get(self):
        self.response.out.write(u"""<h1>集群</h1><p>请访问网盘主网址</p>""")
class ErrorHandler(MyHandler):
    def get(self):
        self.response.out.write(u"""<h1>404 Not Found</h1>""")
class UploadHandler(MyHandler):
    balancer_host = ADDRESS.balancer_host
    balancer_main = balancer_host + "/upload"
    notify_url = balancer_host + "/notify"
    host = ADDRESS.host
    down_url = host + "/download"
    def post(self):
        post_file = self.request.POST["data"]
        tag = self.request.get("tag") or ""
        disk_key = self.request.get("disk_key")
        if not disk_key:
            self.response.out.write("Error: No disk_key given.")
            self.response.set_status(400)
            return
        self.response.out.write(type(post_file))
        new_file = LinkedFile(post_file.filename, post_file.file, tag)
        key = new_file.put()
        
        data = {"size": new_file.size, "filename": new_file.filename.encode("utf8"), "url": "%s?key=%s" %(self.down_url, key), "tag": new_file.tag, "disk_key": disk_key}
        import urllib
        from google.appengine.api import urlfetch
        encoded_data = urllib.urlencode(data)
        result = None
        for i in range(3):
            try:
                result = urlfetch.fetch(url = self.notify_url, payload = encoded_data, method = urlfetch.POST)
                if result.status_code == 200:
                    break
            except:
                continue
        if (not result) or result.status_code != 200:
            self.response.out.write(u"服务器内部错误,请联系管理员.")
        else:
            self.redirect(self.balancer_main)
        #self.response.out.write(u"""<a href="download?key=%s">下载地址(请右键保存链接,留作以后下载)</a><br>""" %key)
class DownloadHandler(MyHandler):
    def get(self):
        key = self.request.get("key")
        if not key:
            return
        file = File.get(db.Key(key))
        if not file:
            self.response.out.write("File not Found. Maybe it has been removed.")
            return 
        import mimetypes
        mime = mimetypes.guess_type(file.filename)
        mime = mime[0] or "application/octet-stream"
        self.response.headers['Content-Type'] = mime
        import urllib
        self.response.headers['Content-Disposition'] = "attachment; filename=%s" % urllib.quote(file.filename.encode("utf8"))
        node = file.head.next
        while node:
            self.response.out.write(node.data)
            node = node.next
def main():
    application = webapp.WSGIApplication([('/', MainHandler), ('/upload', UploadHandler), ('/download', DownloadHandler), ('/.*', ErrorHandler), ],
                                         debug=True)
    util.run_wsgi_app(application)

if __name__ == '__main__':
    main()
