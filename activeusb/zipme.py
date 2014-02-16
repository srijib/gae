#!/usr/bin/python
import zipfile
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
def zipcb(nothing, path, filenames):
    for filename in filenames:
        fullpath = os.path.join(path, filename)[2:]
        if os.path.isdir(fullpath): continue
        print fullpath
        zf.writestr(fullpath, open(fullpath).read())
    return
def main():
    global total_size
    total_size = 0
    #zf = zipfile.ZipFile("../name.zip", "w", zipfile.ZIP_DEFLATED)
    #os.path.walk(".", zipcb, None)
    #zf.close()
    os.path.walk(".", sizecb, None)
    print total_size
if __name__ == "__main__":
    main()
    