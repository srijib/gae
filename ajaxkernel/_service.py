#-*- coding: utf-8 -*-
import urllib2
from google.appengine.ext import webapp
from google.appengine.ext.webapp import util
import logging
class FetionHandler(webapp.RequestHandler):
    API = "http://smsender.sinaapp.com/fetion/api.php"
    def RPC(self, payload):
        logging.debug(
            'Serivce.Fetion.RPC: Will send messages with API("%s") payload("%s").'
            %(self.API, payload)
        )
        result = urllib2.urlopen(self.API, payload)
        content = result.read()
        self.error(result.code) # header must be set first
        self.response.out.write(content)
    def get(self):
        self.RPC(self.request.query_string)
    def post(self):
        self.RPC(self.request.body)

def main():
    application = webapp.WSGIApplication([('/_service/send/fetion', FetionHandler)],
                                         debug=True)
    util.run_wsgi_app(application)


if __name__ == '__main__':
    main()
