from google.appengine.ext import webapp
from google.appengine.ext.webapp import util
from model import *

class UploadHandler(webapp.RequestHandler):
    def get(self):
        self.response.out.write('Wel.')
    def post(self):
        name = self.request.headers["name"]
        new_desktop = Desktop(name = name)    #
        data = self.request.body
        new_desktop.pic = data
        new_desktop.put()
        from google.appengine.api import taskqueue
        taskqueue.add(url='/send_mail', params={'key': new_desktop.key()})
        self.response.out.write('Wel. Data saved. length: %d' %len(data))
class SendMailHandler(webapp.RequestHandler):
    def post(self):
        key = self.request.get('key')
        key = db.Key(key)
        desktop = db.get(key)
        if not desktop:
            self.error(500)
            return
        from google.appengine.api import mail
        import datetime
        import zlib
        desktop_time = desktop.time + datetime.timedelta(hours=8)
        mail.send_mail(
                        sender = "lihaohua90@gmail.com",
                        to = "lhh1990 <lhh1990@gmail.com>",
                        subject = "DESKTOP: %s"%desktop.name,
                        body = "DESKTOP\nname: %s\ntime:%s" %(desktop.name, desktop_time.strftime("%Y.%m.%d %H:%M:%S")),
                        attachments=[(desktop_time.strftime("%Y%m%d%H%M%S.png"), zlib.decompress(desktop.pic) )]
                        )
        db.delete(desktop)
class GetIntervalHandler(webapp.RequestHandler):
    def get(self):
        name = self.request.headers["name"]
        interval = Interval.all().filter("name =", name).order("-time").get()
        if interval:
            self.response.out.write('%d' %interval.interval)
        else:
            self.response.out.write("no one.")
class SetIntervalHandler(webapp.RequestHandler):
    def get(self):
        name = self.request.get("name")
        interval = self.request.get("interval")
        if not name:
            self.response.out.write('no name given')
            return
        try:
            interval = int(interval)
        except:
            self.response.out.write('no right interval given')
            return
        interval_record = Interval.all().filter("name =", name).order("-time").get()
        if interval_record:
            interval_record.interval = interval
            interval_record.put()
        else:
            interval_record = Interval(name=name, interval = interval)
            interval_record.put()
            self.response.out.write("new interval infomation created.")
        self.response.out.write('interval saved : %d seconds.' %interval_record.interval)

class GetHandler(webapp.RequestHandler):
    def get(self):
        name = self.request.get("name")
        try:
            limit = int(self.request.get("limit"))
        except:
            limit = None
        try:
            offset = int(self.request.get("offset"))
        except:
            offset = None
        
        if name and limit and offset:
            desktops = Desktop.all().filter("name = ", name).order("-time").fetch(limit, offset)
        elif name and limit:
            desktops = Desktop.all().filter("name = ", name).order("-time").fetch(limit)
        elif name and offset:
            desktops = Desktop.all().filter("name = ", name).order("-time").fetch(limit=1000, offset=offset)
        elif name:
            desktops = Desktop.all().filter("name = ", name).order("-time")
        else:
            self.response.out.write('no name given')
            return
        if desktops:
            self.response.out.write( "<h1>%s</h1>" %name )
            for desktop in desktops:
                self.response.out.write( """<a href="/getbykey?key=%s">%s</a><br>""" %(desktop.key(), desktop.time) )
        else:
            self.response.out.write('No ones.')

class GetByTimeHandler(webapp.RequestHandler):
    def get(self):
        name = self.request.get("name")
        from_time = self.request.get("from")
        to_time = self.request.get("to")
        if not name:
            self.response.out.write('no name given')
        import datetime
        try:
            from_time = eval(from_time)
            to_time = eval(to_time)
            from_time = datetime.datetime(*from_time)
            to_time = datetime.datetime(*to_time)
        except:
            self.response.out.write('can\'t parse and convert time format: from_time and to_time.')
            return
        
        desktops = Desktop.all().filter("name = ", name).filter("time >= ", from_time).filter("time < ", to_time).order("-time")
        if desktops:
            self.response.out.write( "<h1>%s</h1>" %name )
            for desktop in desktops:
                self.response.out.write( """<a href="/getbykey?key=%s">%s</a><br>""" %(desktop.key(), desktop.time) )
        else:
            self.response.out.write('No ones.')

class GetZipHandler(webapp.RequestHandler):
    def get(self):
        name = self.request.get("name")
        from_time = self.request.get("from")
        to_time = self.request.get("to")
        if not name:
            self.response.out.write('no name given.')
        import datetime
        try:
            from_time = eval(from_time)
            to_time = eval(to_time)
            from_time = datetime.datetime(*from_time)
            to_time = datetime.datetime(*to_time)
        except:
            self.response.out.write('can\'t parse and convert time format: from_time and to_time.')
            return
        
        desktops = Desktop.all().filter("name = ", name).filter("time >= ", from_time).filter("time < ", to_time).order("-time")
        
        if desktops:
            import cStringIO, zipfile, zlib, datetime
            ostream = cStringIO.StringIO()
            z = zipfile.ZipFile(ostream, "wb")
            for desktop in desktops:
                filename = (desktop.time + datetime.timedelta(hours=8)).strftime("%Y%m%d%H%M%S.png")
                z.writestr(filename, zlib.decompress(desktop.pic))
            z.close()
            self.response.headers['Content-Type'] = 'application/zip'
            self.response.headers['Content-Disposition'] = "attachment; filename=out.zip"
            self.response.out.write(ostream.getvalue())
        else:
            self.response.out.write('No ones.')
class GetByKeyHandler(webapp.RequestHandler):
    def get(self):
        key = self.request.get("key")
        #from google.appengine.ext import db
        if key:
            desktop = Desktop.get(key)
        else:
            self.response.out.write('no key given')
            return
        if desktop:
            import datetime
            self.response.headers['Content-Type'] = "image/png"
            self.response.headers['Content-Disposition'] = "attachment; filename=%s" %(desktop.time + datetime.timedelta(hours=8)).strftime("%Y%m%d%H%M%S.png")
            import zlib
            self.response.out.write( zlib.decompress(desktop.pic) )
        else:
            self.response.out.write('Err.')

def main():
    application = webapp.WSGIApplication([('/upload', UploadHandler), ('/get', GetHandler), ('/getbytime', GetByTimeHandler), ('/getzip', GetZipHandler), ('/getbykey', GetByKeyHandler), ('/getinterval', GetIntervalHandler), ('/setinterval', SetIntervalHandler), ('/send_mail', SendMailHandler), ],
                                         debug=True)
    util.run_wsgi_app(application)


if __name__ == '__main__':
    main()
