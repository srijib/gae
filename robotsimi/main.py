#!/usr/bin/env python
# -*- coding: utf8 -*-
# 单文件 app
import webapp2
import urllib, urllib2, json, logging, traceback, random

def chat(msg):
    no_list = ['切,不理你了!', '=_=', '小鸡鸡现在很忙', '不鸟你', '真无语', '好吧,折服了', '.']
    # msg is utf8 str
    msg = msg.strip()
    if not msg: return "跟我说说话吧~"
    # else msg is not empty
    ua = 'Mozilla/5.0 (Linux; Android 4.1.1; Nexus 7 Build/JRO03D) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.166 Safari/535.19'
    req = urllib2.Request('http://m.simsimi.com/talk.htm')
    req.add_header('User-Agent', ua)
    r = urllib2.urlopen(req)
    #print dir(r)
    cookie = r.headers["Set-Cookie"]
    content = r.read()
    #print content
    qt = urllib.quote
    msg = qt(qt(msg))
    req = urllib2.Request("http://m.simsimi.com/func/req?msg=%s&lc=zh" %msg)
    req.add_header('Referer', 'http://m.simsimi.com/talk.htm')
    req.add_header('User-Agent', ua)
    req.add_header('Cookie', 'sagree=true; ' + cookie)
    r = urllib2.urlopen(req)
    content = r.read()
    result = json.loads(content)
    if 'response' in result:
        return result['response'].encode('utf8')
    else:
        logging.error('Error, response: ' + content)
        return random.choice(no_list)
class MainHandler(webapp2.RequestHandler):
    def get(self):
        self.response.write('Hello Robot!')

class ChatHandler(webapp2.RequestHandler):
    def get(self, msg):
        try:
            resp = chat(msg)
            logging.info("A: {%s}, B: {%s}" %(msg, resp))
        except Exception:
            resp = "Sorry,小鸡鸡咯屁了! :("
            errorMsg = traceback.format_exc()
            logging.error("Error: " + errorMsg)
        self.response.write(resp)

app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/chat/(.*)', ChatHandler)
], debug=True)
