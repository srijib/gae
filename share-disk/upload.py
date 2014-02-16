#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
from google.appengine.ext import webapp
from google.appengine.ext.webapp import util
from models import *

class MainHandler(webapp.RequestHandler):
    def get(self):
        self.response.out.write(u"""<h1>上传到共享网盘</h1>
<form method="post" action="upload" enctype="multipart/form-data"><input type="file" name="data" /><input type="submit" value="上传" /></form><span style="color:#F00;font-size:12px">注:文件最大10M,类型不限</span><br>""")
        self.response.out.write(u"<h4>文件列表:</h4>")
        self.response.out.write(u"""<table style="font-size:12px">""")
        import datetime
        for file in File.all().order('-time').fetch(1000):
            self.response.out.write(u"""<tr><td>%s</td><td>%s</td><td><a href="download?key=%s">下载</a></td></tr>""" 
                %(file.filename, ( file.time + datetime.timedelta(hours=8) ).strftime ("%Y-%m-%d %H:%M"), file.key(),) 
                )
        self.response.out.write(u"""</table>""")
    def post(self):
        filename = self.request.POST["data"].filename
        content = self.request.get("data")
        new_file = LinkedFile(filename, content)
        key = new_file.put()
        self.response.out.write(u"""<a href="download?key=%s">下载地址(请右键保存链接,留作以后下载)</a>""" %key)
def main():
    application = webapp.WSGIApplication([('/upload', MainHandler)],
                                         debug=True)
    util.run_wsgi_app(application)


if __name__ == '__main__':
    main()
