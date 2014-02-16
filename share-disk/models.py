#!/usr/bin/env python
from google.appengine.ext import db
class Node(db.Model):
    data = db.BlobProperty()
    next = db.SelfReferenceProperty()
class File(db.Model):
    filename = db.StringProperty(required=True)
    head = db.ReferenceProperty(Node, required=True)
    time = db.DateTimeProperty(auto_now = True)

class LinkedFile:
    def __init__(self, filename, content):
        self.maxSize = int(0.99*1024*1024)
        self.filename = filename
        self.content = content
    def put(self):
        if not self.content:
            return
        from StringIO import StringIO
        sio = StringIO(self.content)
        last_node = Node()
        last_node.put()
        file = File(filename = self.filename, head = last_node)
        file.put()
        while True:
            sss = sio.read(self.maxSize)
            if not sss:
                break
            else:
                node = Node(data = sss)
                node.put()
                last_node.next = node
                last_node.put()
                last_node = node
        return str(file.key())
