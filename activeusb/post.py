#-*- coding: utf-8 -*-
#!/usr/bin/env python

from google.appengine.ext import webapp
from google.appengine.ext.webapp import util
from model import Code
class PostHandler(webapp.RequestHandler):
    def post(self):
        code_content = self.request.get("code")
        name = self.request.get("name")
        if not code_content or not name:
            self.response.out.write("No Name or Content")
            return
        code = Code(language="python", name = name, code = code_content)
        code.put()
        self.response.out.write('%s saved' %name)
def main():
    application = webapp.WSGIApplication([('/.*', PostHandler)],
                                         debug=True)
    util.run_wsgi_app(application)



if __name__ == '__main__':
    main()
