#!/usr/bin/env python
from google.appengine.ext import db

class Node(db.Model):
    data = db.BlobProperty()
    next = db.SelfReferenceProperty()

class File(db.Model):
    filename = db.StringProperty(required=True)
    size = db.IntegerProperty(required = True)
    tag = db.StringProperty(default = "")
    head = db.ReferenceProperty(Node, required=True)
    time = db.DateTimeProperty(auto_now = True)
    
class LinkedFile:
    def __init__(self, filename, content, tag):
        self.maxSize = 1000*1000
        self.filename = filename
        self.content = content
        self.tag = tag
        self.size = len(self.content.getvalue())
    def put(self):
        if not self.content:
            return None
        sio = self.content
        last_node = Node()
        last_node.put()
        file = File(filename = self.filename, size = self.size, tag = self.tag, head = last_node)
        file.put()
        while True:
            part_content = sio.read(self.maxSize)
            if not part_content:
                break
            else:
                node = Node(data = part_content)
                node.put()
                last_node.next = node
                last_node.put()
                last_node = node
        return str(file.key())
