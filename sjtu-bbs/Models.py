#-*- coding: utf-8 -*-
#!/usr/bin/env python
from google.appengine.ext import db

class Page(db.Model):
    url = db.LinkProperty()
    html = db.BlobProperty()
    # zlib compressed
    indexed = db.BooleanProperty(default = False)
    add_time = db.DateTimeProperty( auto_now = True )

class SuperQueue(db.Model):
    subqueue = db.ListProperty(db.Text, default=[])
    add_time = db.DateTimeProperty( auto_now_add = True )
    mod_time = db.DateTimeProperty( auto_now = True )
    __MAXSIZE = 2000
    __last_record = None
    __modified = False
    @classmethod
    def is_empty(cls):
        cls.__get_last_record()
        return (len(cls.__last_record.subqueue) == 0)
    @classmethod
    def __get_last_record(cls):
        if not cls.__last_record:
            cls.__last_record = cls.all().order("-mod_time").get()
            # order("-add_time") is also ok?
            if not cls.__last_record:
                new_record = cls()
                cls.__last_record = new_record
                cls.__modified = True
    @classmethod
    def append(cls, item):
        cls.__get_last_record()
        cls.__last_record.subqueue.append(item)
        if len(cls.__last_record.subqueue) >= cls.__MAXSIZE:
            cls.save()
            new_record = cls()
            cls.__last_record = new_record
            cls.__last_record.subqueue.append(item)
        else:
            pass
        cls.__modified = True
        return True
    @classmethod
    def dequeue(cls):
        cls.__get_last_record()
        if cls.__last_record.subqueue:
            item = cls.__last_record.subqueue.pop(0)
            cls.__modified = True
            if not cls.__last_record.subqueue:
                #now a empty list
                cls.__last_record.put()
                cls.__last_record.delete()
                cls.__last_record = None
                cls.__get_last_record()
            return item
        else:
            return None
    @classmethod
    def save(cls):
        cls.__get_last_record()
        if cls.__modified and cls.__last_record:
            cls.__last_record.put()
            cls.__modified = False
            return True
        else:
            return False
class Dump(db.Model):
    import marshal
    data = db.BlobProperty( default = marshal.dumps([]) )
    add_time = db.DateTimeProperty(auto_now = True)
    __last_record = None
    __hash_list = None
    __last_record_modified = False
    __hash_list_modified = False
    @classmethod
    def __get_last_record(cls):
        if not cls.__last_record:
            cls.__last_record = cls.all().order("-add_time").get()
            if not cls.__last_record:
                cls.__last_record = cls()
            cls.__last_record_modified = True
        if not cls.__hash_list:
            cls.__hash_list = cls.marshal.loads(cls.__last_record.data)
            cls.__hash_list_modified = True
    @classmethod
    def contains(cls, hash_key):
        cls.__get_last_record()
        return (hash_key in cls.__hash_list)
    @classmethod
    def get_length(cls):
        cls.__get_last_record()
        return len(cls.__hash_list)
    @classmethod
    def add(cls, hash_key):
        cls.__get_last_record()
        if isinstance(hash_key, str):
            hash_key = hash(hash_key)
        if not isinstance(hash_key, int):
            return False
        else:
            if not (hash_key in cls.__hash_list):
                cls.__hash_list.append(hash_key)
                cls.__hash_list_modified = True
                return True
            else:
                return False
    @classmethod
    def save(cls):
        cls.__get_last_record()
        if cls.__hash_list_modified:
            cls.__last_record.data = cls.marshal.dumps(cls.__hash_list)
            cls.__last_record_modified = True
        if cls.__last_record_modified:
            cls.__last_record.put()
class Index(db.Model):
    word = db.StringProperty()
    page = db.ListProperty(db.Key)
