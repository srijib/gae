#!/usr/bin/env python
# -*- coding:utf8 -*-
import random
from django.utils import simplejson
from google.appengine.api import users, memcache
from google.appengine.api.channel import channel
from google.appengine.ext import webapp
from google.appengine.ext.webapp import util
from google.appengine.ext.webapp import template

def send_to_all(message, tokens=None):
    if not tokens:
        tokens = memcache.get('tokens')
    if tokens:
        for token, id in tokens.iteritems():
            if isinstance(id ,int):
                id = 'anonymous(%s)' %id
            channel.send_message(id, message)
class MainHandler(webapp.RequestHandler):
    def get(self):
        template_values = {}
#        self.response.out.write(template.render(path, template_values))
        self.response.out.write(template.render('index.html', template_values))
class GetTokenHandler(webapp.RequestHandler):
    def get(self):
        user = users.get_current_user()
        if user:
            channel_id = id = user.email()
        else:
            id = random.randint(1, 10000)
            channel_id = 'anonymous(%s)' %id
        token = channel.create_channel(channel_id)
        tokens = memcache.get('tokens') or {}
        tokens[token] = id
        memcache.set('tokens', tokens)
        self.response.out.write(token)
class OpenHandler(webapp.RequestHandler):
    def post(self):
        token = self.request.get('token')
        if not token:
            return
        tokens = memcache.get('tokens')
        if tokens:
            id = tokens.get(token, '')
            if id:
                if isinstance(id, int):
                    user_name = u'天朝匿名用户(%s)' % id
                else:
                    user_name = id.split('@')[0]
                message = user_name + u'加入了聊天室'
                message = simplejson.dumps(message)
                send_to_all(message)
class ReceiveHandler(webapp.RequestHandler):
    def post(self):
        token = self.request.get('token')
        if not token:
            return
        message = self.request.get('content')
        if not message:
            return
        tokens = memcache.get('tokens')
        if tokens:
            id = tokens.get(token, '')
            if id:
                if isinstance(id, int):
                    user_name = u'天朝匿名用户(%s)' % id
                else:
                    user_name = id.split('@')[0]
                message = '%s: %s' % (user_name, message)
                message = simplejson.dumps(message)
                if len(message) > channel.MAXIMUM_MESSAGE_LENGTH:
                    return
                send_to_all(message)
def main():
    application = webapp.WSGIApplication([('/', MainHandler), ('/get_token', GetTokenHandler), ('/open', OpenHandler), ('/post_msg', ReceiveHandler), ],
                                         debug=True)
    util.run_wsgi_app(application)


if __name__ == '__main__':
    main()
