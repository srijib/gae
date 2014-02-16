import ConfigParser
from PIL import ImageGrab
import time, httplib
import zlib
import sys, os
config = ConfigParser.ConfigParser()
path = os.path.dirname(sys.argv[-1])
full_path = os.path.join(path, "cap.conf")
config.read(full_path)
name = config.get("config", "name")
url = config.get("config", "url")
print name

try:
    preconf_interval = int( config.get("config", "interval") )
except:
    preconf_interval = 120

def get_fresh_interval():
    global url, name, preconf_interval
    try:
        conn = httplib.HTTPConnection(url)
        conn.request("GET", "/getinterval", headers={"name": name})
        res = conn.getresponse()
        interval = int(res.read())
    except:
        #print sys.exc_info()
        interval = preconf_interval
    return interval
#end of  get_fresh_interval()
interval = get_fresh_interval()
print "interval: %d" %interval
cycle_time = time.time()
try:
    conn = httplib.HTTPConnection(url)
    conn.request("GET", "/poweron", headers={"name": name})
    res = conn.getresponse()
except:
    pass
while(True):
    a = ImageGrab.grab()
    a.save("normal.png")
    
    data = open("./normal.png", "rb")
    data_s = data.read()
    #print len(data_s)
    data_s = zlib.compress(data_s)
    data.close()
    #print len(data_s)
    params = data_s
    try:
        conn = httplib.HTTPConnection(url)
        conn.request("POST", "/upload", params, {"name": name})
        res = conn.getresponse()
        print res.status, res.reason
        print res.read()
        conn.close()
    except:
        print "error:"#, sys.exc_info()
    print time.strftime("%Y-%m-%d %H:%M:%S")
    time.sleep(interval)
    if (time.time()-cycle_time) > 120:
        interval = get_fresh_interval()
        print " INFO: new interval: %d" %interval
        cycle_time = time.time()
pass
