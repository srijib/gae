#!/usr/bin/python
import os, sys
def sizecb(nothing, path, filenames):
    global total_size
    for filename in filenames:
        fullpath = os.path.join(path, filename)[2:]
        if os.path.isdir(fullpath): continue
        size = os.path.getsize(fullpath)
        print fullpath, size
        total_size += size
    return
def m():
    global total_size
    total_size = 0
    os.path.walk(".", sizecb, None)
    #/base/python_runtime/python_lib/versions/1
    print total_size
if __name__ == "__main__":
    m()
