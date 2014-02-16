#!/usr/bin/env python
#-*- coding: utf-8 -*-

__author__ = 'ZWdnZmx5QHFxLmNvbQ==\n'.decode('base64')
__version__ = '0.0.1'

from util import crypto, httpheaders
import cPickle as pickle
import zlib, logging, time, re, struct
from google.appengine.ext import webapp, db
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.api import urlfetch, memcache
from google.appengine.runtime import apiproxy_errors
urlfetch._CaselessDict = httpheaders.HTTPHeaders

from gaeproxy import MainHandler
from gaeproxy2 import MainHandler as MainHandler_Redirect

class WPConfig(db.Model):
    cfgCacheTime = db.IntegerProperty(required=True, default=5*60)
    cacheTime = db.IntegerProperty(default=24*3600)
    maxSize = db.IntegerProperty(required=True, default=9000000)
    mixSize = db.IntegerProperty(default=100000)
    siteKey = db.StringProperty(default=u'')
    cryptoMode = db.StringProperty(default=u'XOR--32')
    version = db.StringProperty()

def getConfig():
    config = memcache.get('config', namespace='wp_config')
    if config is None:
        cfg = WPConfig.all().get()
        if not cfg:#No Entry
            cfg = WPConfig(version=__version__)
            cfg.put()
        elif cfg.version < __version__:
            cfg = WPConfig(key=cfg.key(), siteKey=cfg.siteKey,
                    cryptoMode=cfg.cryptoMode, version=__version__)
            cfg.put()
            memcache.flush_all()
        config = {'cacheTime':cfg.cacheTime, 'maxSize':cfg.maxSize,
                  'siteKey':cfg.siteKey.encode('utf-8').decode('string_escape'),
                  'crypto':cfg.cryptoMode.encode('utf-8'), 'mixSize':cfg.mixSize}
        if not memcache.set('config', config, cfg.cfgCacheTime, namespace='wp_config'):
            logging.error('Memcache set wp_config failed')
    return config

def _init_config(crypto_cls):
    config = getConfig()
    config['crypto'] = crypto_cls(config['crypto'])
    return config

def isNormal():
    from time_control_config import *
    local_vars = locals()
    if not local_vars.has_key("in_section_direct"): in_section_direct = True
    if not local_vars.has_key("everyday_sections"): everyday_sections = []
    if not local_vars.has_key("datetime_sections"): datetime_sections = []
    del local_vars
    import datetime, time
    
    # 获得当前datetime (+8:00 东8时区)
    now = datetime.datetime.utcnow() + datetime.timedelta(hours = 8)
    # 初始化
    in_section = False
    
    # 判断特殊日期时间的区间, 优先级最高
    datetime_format_without_second = "%Y.%m.%d %H:%M"
    datetime_format_with_second = "%Y.%m.%d %H:%M:%S"
    for (start_time_str, end_time_str) in datetime_sections:
        start_time = None
        end_time = None
        # try parse datetime with or without second
        try:
            start_time = datetime.datetime.strptime(start_time_str, datetime_format_with_second)
        except: pass
        if (start_time is None):
            try:
                start_time = datetime.datetime.strptime(start_time_str, datetime_format_without_second)
            except: pass
        try:
            end_time = datetime.datetime.strptime(end_time_str, datetime_format_with_second)
        except: pass
        if (end_time is None):
            try:
                end_time = datetime.datetime.strptime(end_time_str, datetime_format_without_second)
            except: pass
        if (start_time is None) or (end_time is None): continue
        if start_time < now < end_time: # here is now
            in_section = True
            break
    
    # 取得时间信息
    now_time = now.time()
    # 判断每日循环的区间, 优先级稍低
    if not in_section:
        for (start_time_str, end_time_str) in everyday_sections:
            start_time_tuple = [int(str_time) for str_time in start_time_str.split(":")]
            end_time_tuple = [int(str_time) for str_time in end_time_str.split(":")]
            start_time = datetime.time(*start_time_tuple)
            end_time = datetime.time(*end_time_tuple)
            if start_time < now_time < end_time:    # here is now_time
                in_section = True
                break
    
    if (in_section and (in_section_direct == False)) or ((not in_section) and (in_section_direct == True)):
        return True
    else:
        return False

def run_main(cls):
    run_wsgi_app(webapp.WSGIApplication([(r'/.*', cls)], debug=True))

def main():
    if isNormal():
        run_main(MainHandler)
    else:
        run_main(MainHandler_Redirect)

if __name__ == '__main__':
    main()
