import imp
import sys
from google.appengine.ext import db
from google.appengine.ext import gql
from model import File

def db_import(name, globals=None, locals=None, fromlist=None):
    # Fast path: see if the module has already been imported.
    try:
        return sys.modules[name]
    except KeyError:
        pass
    # load modules from other places
    query = db.GqlQuery('select * from File where name=:1', '%s.py' %name)
    if query.count() > 0:
        file_obj = query.fetch(1)[0]
        codeStr = file_obj.content
        extra_module = imp.new_module(name)
        exec codeStr in extra_module.__dict__
        sys.modules[name] = extra_module
        return extra_module
    # If any of the following calls raises an exception,
    # there's a problem we can't handle -- let the caller handle it.
    fp, pathname, description = imp.find_module(name)
    try:
        return imp.load_module(name, fp, pathname, description)
    finally:
        # Since we may exit via an exception, close fp explicitly.
        if fp:
            fp.close()

