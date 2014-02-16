#-*- coding: utf-8 -*-
#!/usr/bin/env python
from google.appengine.ext import webapp
from google.appengine.ext.webapp import util

class MainHandler(webapp.RequestHandler):
    def get(self):
        self.response.out.write('cron')
class CheckAliveHandler(webapp.RequestHandler):
    def get(self):
        #from model import Data
        #if Data.all().filter("url =", ).count() == 0:
        #   data = Data
        check_list = [
        ("http://www.cloudrive.tk/", u"www.cloudrive.tk"),
        ("http://blog.cloudrive.tk/", u"blog.cloudrive.tk"),
        ("http://code.cloudrive.tk/", u"code.cloudrive.tk"),
        ("http://desktop.cloudrive.info/", u"desktop.cloudrive.info"),
        ("http://desktop.cloudrive.tk", u"desktop.cloudrive.tk"),
        ("http://www.app-ark.com", u"app-ark.com"),
        ("http://211.80.62.40:8000/hain/","http://211.80.62.40:8000/hain/")
        ]
        if self.request.get('nosend'):
            sendmail = False
        else:
            sendmail = True
        from google.appengine.api import mail
        from google.appengine.api import urlfetch
        self.response.headers["Content-Type"] = "text/plain"
        self.response.out.write('Check Alive\n')
        allmsg = []
        for pair in check_list:
            try:
                for i in range(3):
                    result = urlfetch.fetch(pair[0])
                    if result.status_code == 200:
                        msg = u"OK"
                        break
            except:
                msg = u"Err"
            allmsg.append(pair[1]+u" "+msg)
        mailbody = u"\n".join(allmsg)
        # debug
        self.response.out.write(mailbody)
        if sendmail:
            # mail.send_mail(sender_address, user_address, subject, body)
            mail.send_mail("lihaohua90@gmail.com", "13821254203@139.com", u"[Server Status Reports]", mailbody)
            self.response.out.write('\nMail Sent!\n')
class FetchUrlHandler(webapp.RequestHandler):
    def get(self):
        check_list = [
        ("http://cloudrive.tk", u"http://cloudrive.tk"),
        ("http://eggfly.tk", u"http://eggfly.tk"),
        ("http://sjtubbs.tk", u"http://sjtubbs.tk"),
        ("http://tangtoday.tk", u"http://tangtoday.tk"),
        ("http://pyide.tk", u"http://pyide.tk"),
        ]
        from google.appengine.api import urlfetch
        self.response.headers["Content-Type"] = "text/plain"
        self.response.out.write('Fetch URL\n')
        allmsg = []
        for pair in check_list:
            try:
                for i in range(3):
                    result = urlfetch.fetch(pair[0])
                    if result.status_code == 200:
                        msg = u"OK"
                        break
            except:
                msg = u"Err"
            allmsg.append(pair[1]+u" "+msg)
        mailbody = u"\n".join(allmsg)
        # debug
        self.response.out.write(mailbody)
        self.response.out.write('\nOK!\n')
def main():
    application = webapp.WSGIApplication([('/', MainHandler), ("/checkalive.py", CheckAliveHandler), ("/fetchurl.py", FetchUrlHandler)],
                                         debug=True)
    util.run_wsgi_app(application)


if __name__ == '__main__':
    main()
