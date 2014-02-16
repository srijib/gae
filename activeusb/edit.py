#-*- coding: utf-8 -*-
#!/usr/bin/env python

from google.appengine.ext import webapp
from google.appengine.ext.webapp import util
from model import Code
class EditHandler(webapp.RequestHandler):
    def get(self, name):
        #print name
        #print len(name)
        import os, urllib
        from google.appengine.ext.webapp import template
        name = urllib.unquote(name).decode("utf8")
        template_values = {
        }
        if name:
            code = Code.all().filter("name =", name).get()
            if not code:
                self.response.out.write("Error: No such file")
                return
            template_values["code"] = code.code
            template_values["name"] = code.name
        else:
            import time
            template_values["name"] = "%d.py" %time.time()
        # 没有name时, template_values为空
        path = os.path.join(os.path.dirname(__file__), 'editor.html')
        self.response.out.write(template.render(path, template_values))


def edit_main():
    application = webapp.WSGIApplication([(r'/edit()', EditHandler), (r'/edit/(.*)$', EditHandler)],
                                         debug=True)
    util.run_wsgi_app(application)



if __name__ == '__main__':
    edit_main()
