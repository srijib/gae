#!/usr/bin/env python

import sys
import cgi
import datetime
import wsgiref.handlers
import zlib

import re

import urllib
from google.appengine.ext import webapp
from google.appengine.api import urlfetch

class Proxy(webapp.RequestHandler):
  def get(self):
    return doProxy(self, 'GET')
  def post(self):
    return doProxy(self, 'POST')

application = webapp.WSGIApplication([
  ('/.*', Proxy),
], debug=True)

def doProxy(self, methed):
  #url
  proxy_url = urllib.unquote(self.request.url)
  reobj     = re.compile(r'^https?://(([^/\:]+)([^/]+)?)/',re.S|re.M|re.I)
  m = reobj.match(proxy_url)
  host = m.group(1)
  host_name = m.group(2)
  proxy_url = reobj.sub('', proxy_url)

  reobj     = re.compile(r'^(?:https?://)?([^/]+)(/?)(.*)',re.S|re.M|re.I)
  m = reobj.match(proxy_url)
  proxy_host = m.group(1)
  proxy_url = 'http://' + m.group(1) + m.group(2) + m.group(3)
  
  if m.group(2) == '':
    self.response.set_status(301)
    sys.stdout.write('Status: 301 Moved Permanently\r\n')
    sys.stdout.write('Location: https://' + host + '/'+proxy_host+'/\r\n')
    return
  #fix header
  self.request.headers['Accept-Encoding'] = ''
  #self.request.headers['Referer'] = ''

  try:
    payload = None
    if methed=='POST':
      payload = self.request.body

    result = urlfetch.fetch(proxy_url, payload, methed , self.request.headers, False, False)

  except urlfetch.InvalidURLError, e:
    self.response.set_status(500)
    self.response.out.write(str(e))
    return
  except urlfetch.DownloadError, e:
    self.response.set_status(404)
    self.response.out.write(str(e))
    return
  except urlfetch.ResponseTooLargeError, e:
    self.response.set_status(301)
    sys.stdout.write('Status: 301 Moved Permanently\r\n')
    sys.stdout.write('Location: '+proxy_url+'\r\n')
    return
  except urlfetch.Error, e:
    self.response.set_status(500)
    self.response.out.write(str(e))
    return

  self.response.set_status(result.status_code)

  if 'location' in result.headers.caseless_keys:
    reobj     = re.compile(r'^\s*(http)s?://(.*)$',re.S|re.M|re.I)
    result.headers['location'] = reobj.sub('\\1://'+host+'/\\2', result.headers['location'])
    reobj     = re.compile(r'^\s*/(.*)$',re.S|re.M|re.I)
    result.headers['location'] = reobj.sub('/'+proxy_host+'/\\1', result.headers['location'])
    sys.stdout.write('Location: '+result.headers['location']+'\r\n')
    return
  
  content = result.content
  #ungzip
  if 'content-encoding' in result.headers.caseless_keys:
    content = zlib.decompress(content)

  #fix abs url
  reobj     = re.compile(r'\s*(href|src|action)\s*=\s*(?:"|\')?\s*(http)s?://([^ <>"\']*)\s*(?:"|\')?',re.S|re.M|re.I)
  content = reobj.sub(' \\1="\\2://'+host+'/\\3"', content)
  #fix rel url
  reobj     = re.compile(r'\s*(href|src|action)\s*=\s*(?:"|\')?\s*/([^ <>"\']*)\s*(?:"|\')?',re.S|re.M|re.I)
  content = reobj.sub(' \\1="/'+proxy_host+'/\\2"', content)
  #fix css bg abs url
  reobj     = re.compile(r'\s*(url)\s*\(\s*(http)s?://([^ <>"\']*)\s*\)',re.S|re.M|re.I)
  content = reobj.sub(' \\1(\\2://'+host+'/\\3)', content)
  #fix css bg rel url
  reobj     = re.compile(r'\s*(url)\s*\(\s*/([^ <>"\']*)\s*\)',re.S|re.M|re.I)
  content = reobj.sub(' \\1(/'+proxy_host+'/\\2)', content)

  if 'set-cookie' in result.headers.caseless_keys:
    reobj     = re.compile(r'(.*path\s*=\s*)(.*)',re.S|re.M|re.I)
    #result.headers['set-cookie'] = reobj.sub('\\1/'+ proxy_host +'\\2', result.headers['set-cookie'])
    result.headers['set-cookie'] = reobj.sub('\\1/', result.headers['set-cookie'])
    reobj     = re.compile(r'domain\s*=\s*[0-9z-zA-Z_\.]+',re.S|re.M|re.I)
    result.headers['set-cookie'] = reobj.sub('domain=' + host_name, result.headers['set-cookie'])

    if result.headers['set-cookie'] != '':
      self.response.headers.add_header('set-cookie', result.headers['set-cookie'])
      sys.stdout.write('set-cookie: %s\r\n' % result.headers['set-cookie'])

  reobj     = re.compile(r'.*?<meta.*?content=(?:"|\')?([^<>"\']+)(?:"|\')?.*',re.S|re.M|re.I)
  m = reobj.match(content)
  if m != None:
    self.response.headers.add_header("Content-Type", m.group(1))
    sys.stdout.write('Content-Type: %s\r\n' % m.group(1))
  else:
    self.response.headers.add_header("Content-Type", result.headers['Content-Type'])
    sys.stdout.write('Content-Type: %s\r\n' % result.headers['Content-Type'])

  self.response.out.write(content)

  return True

def main():
  wsgiref.handlers.CGIHandler().run(application)

if __name__ == '__main__':
  main()

