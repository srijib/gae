#!/usr/bin/env python
# -*- coding: utf-8 -*-
from google.appengine.ext import webapp
from google.appengine.ext.webapp import util
from google.appengine.ext.webapp import template
from google.appengine.ext import db
from lib import MyHandler, approximate_size
from models import Disk
class AdminHandler(MyHandler):
    def get(self):
        template_file = {}
        disks = Disk.all().fetch(10000)
        total = Disk.total
        for d in disks:
            d.free_str = approximate_size(total - d.used)
            d.used_str = approximate_size(d.used)
        template_file["disks"] = disks
        self.render("views/admin.html", template_file)
class AddDiskHandler(MyHandler):
    def get(self):
        host = self.request.get("host")
        if not host:
            self.response.out.write(u""""host" not given.""")
            self.response.set_status(405)
            return
        new_disk = Disk(host = host)
        new_disk.put()
        self.response.out.write(u"OK. New host appended: %s" %new_disk.host)
class RemoveDiskHandler(MyHandler):
    def get(self):
        key = self.request.get("key")
        if not key:
            self.response.out.write(u""""key" not given.""")
            self.response.set_status(405)
            return
        disk = Disk.get(db.Key(key))
        disk.delete()
        self.response.out.write(u"OK. host removed.")
def main():
    application = webapp.WSGIApplication([('/admin/?', AdminHandler), ('/admin/add_disk', AddDiskHandler), ('/admin/remove_disk', RemoveDiskHandler),],
                                         debug=True)
    util.run_wsgi_app(application)

if __name__ == '__main__':
    main()
