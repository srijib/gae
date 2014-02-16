#!/usr/bin/env python
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
import os
class MyHandler(webapp.RequestHandler):
    def render(self, template_file, template_value):
        path = os.path.join(os.path.dirname(__file__), template_file)
        self.response.out.write(template.render(path, template_value))

def approximate_size(size):
    SUFFIXES = ['KB', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB', 'YB']
    multiple = 1024.0
    for suffix in SUFFIXES:
        size /= multiple
        if size < multiple:
            return '%.1f%s' %(size, suffix)
    raise ValueError('number too large')
