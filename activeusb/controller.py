#-*- coding: utf-8 -*-
#!/usr/bin/env python

from google.appengine.ext import webapp
from google.appengine.ext.webapp import util
from google.appengine.ext import db
from google.appengine.ext.webapp import template
import cStringIO
import sys, os, traceback

class Code(db.Model):
    language = db.StringProperty()
    code = db.TextProperty(required = True)
    new_time = db.DateTimeProperty(auto_now_add = True)
    mod_time = db.DateTimeProperty(auto_now = True)
    
class DoHandler(webapp.RequestHandler):
    def runcode(self, code_str):
        save_stdout = sys.stdout
        results_io = cStringIO.StringIO()
        try:
            sys.stdout = results_io
            code = code_str.replace("\r\n", "\n")
            try:
                compiled_code = compile(code, '<string>', 'exec')
                exec(compiled_code, globals())
            except Exception, e:
                traceback.print_exc(file=results_io)
        finally:
            sys.stdout = save_stdout
        results = results_io.getvalue()
        return results
    def post(self):
        action = self.request.get("action")
        language = self.request.get("lang")
        code = self.request.get("code_str")
        path = os.path.join(os.path.dirname(__file__), 'output.html')
        values = {}
        if action == "save":
            new_code = Code(language = language, code = code)
            new_code.put()
        elif action == "run":
            values["output"] = self.runcode(code)
        elif action == "save&run":
            new_code = Code(language = language, code = code)
            new_code.put()
            self.runcode(code)
            
        self.response.out.write(template.render(path, values))
def main():
    application = webapp.WSGIApplication([('/do', DoHandler)],
                                         debug=True)
    util.run_wsgi_app(application)

if __name__ == '__main__':
    main()
