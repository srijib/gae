#!/usr/bin/env python

import urllib2, base64
import datetime

def main():
    prefix = 'http://192.168.1.1:10010'
    username = 'eggfly'
    password = 'adminadmin'
    url = prefix + '/userRpm/SysRebootRpm.htm?Reboot=%D6%D8%C6%F4%C2%B7%D3%C9%C6%F7'
    auth = 'Basic ' + base64.b64encode(username+':'+password)
    print datetime.datetime.now().__str__()
    headers = { 'Referer' : prefix + '/userRpm/SysRebootRpm.htm',
             'Authorization' : auth
    }
    request = urllib2.Request(url, None, headers)
    response = urllib2.urlopen(request)
    result = response.read()
    print len(result)
    print
if __name__ == '__main__':
    main()
