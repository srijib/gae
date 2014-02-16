#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import urllib
import time
import datetime
import os
from dnspod.apicn import *

DOMAIN_ID = 3533147
RECORD_ID = 23535497
EMAIL = 'lihaohua90@gmail.com'
PASSWORD = 'Lihaohuaasdf'
FILENAME = 'previous.ip.txt'
def get_remote_ip():
    url = "http://bot.whatismyipaddress.com/"
    req = urllib.urlopen(url)
    result = req.read()
    return result.strip()
def get_previous_ip():
    ip = ''
    if os.path.isfile(FILENAME):
        fp = open(FILENAME)
        ip = fp.read()
        fp.close()
    return ip
def save_ip(ip):
    fp = open(FILENAME, 'w')
    fp.write(ip)
    fp.close()
def set_ddns(ip):
    api = RecordModify(
        domain_id=DOMAIN_ID,
        record_id=RECORD_ID,
        sub_domain='@',
        record_type='A',
        record_line='默认',
        value=ip,
        ttl='120',
        email=EMAIL,
        password=PASSWORD
    )
    return api()

if __name__ == '__main__':
    remote_ip = get_remote_ip()
    previous_ip = get_previous_ip()
    if remote_ip != previous_ip:
        set_ddns(remote_ip)
        print "new ip: %s, time: %s" %(remote_ip, datetime.datetime.now())
        save_ip(remote_ip)
# end

