import urllib
import os
import time

filename = "xiaomi.html"

while True:
    url = "http://www.xiaomi.com/default.html"
    req = urllib.urlopen(url)
    content = req.read();
    print len(content)
    if os.path.exists(filename):
        fp = open(filename)
        file_content = fp.read()
        fp.close()
        if file_content != content:
            email_url = "http://1.alive.sinaapp.com/raspberrypi.php"
            email_req = urllib.urlopen(email_url, data = "http://www.xiaomi.com/default.html")
            email_req.read()
            print "diff found and alert by email"
    # finally
    fp = open(filename, "w")
    fp.write(content)
    fp.close()
    time.sleep(60)
