import os, sys
print sys.argv[0]
pathname = os.path.dirname(sys.argv[0])
print pathname
print os.path.abspath(pathname)
print os.getcwd()