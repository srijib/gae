#!/usr/bin/env python
# -*- coding: utf-8 -*-

from google.appengine.ext import webapp
from google.appengine.ext.webapp import util
class RunHandler(webapp.RequestHandler):
    def post(self):
        import cStringIO
        import sys, traceback
        import os
        from google.appengine.ext.webapp import template
        code = self.request.get("code")
        #print code
        #name = self.request.get("name")
        if not code:
            self.response.out.write("Error: No Code Content")
            return
        save_stdout = sys.stdout
        results_io = cStringIO.StringIO()
        try:
            sys.stdout = results_io

            code = self.request.get('code')
            code = code.replace("\r\n", "\n")
            code+="\n"
            try:
                compiled_code = compile(code, '<string>', 'exec')
                exec(compiled_code, globals())
            except Exception, e:
                traceback.print_exc(file=results_io)
        finally:
            sys.stdout = save_stdout

        results = results_io.getvalue()
        path = os.path.join(os.path.dirname(__file__), 'interactive-output.html')
        self.response.out.write(template.render(path, {'output': results}))
def run_main():
    application = webapp.WSGIApplication([('/.*', RunHandler)],
                                         debug=True)
    util.run_wsgi_app(application)



if __name__ == '__main__':
    run_main()
