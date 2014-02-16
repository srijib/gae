import StringIO
f = open("dict.txt")
s = f.read()
f.close()
import time
t = time.time()
sio = StringIO.StringIO(s)
print time.time() - t
while True:
    sss = sio.read(1024*1024)
    if not sss:
        break
print time.time() - t
