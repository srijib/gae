# encoding: utf-8
from google.appengine.api import memcache
import logging
import conf
class CrawlerManager:
    CRAWLER_MEMCACHE_KEY = 'obj_crawler'
    crawler = None
    @classmethod
    def store_in_memcache(cls):
        memcache.set(cls.CRAWLER_MEMCACHE_KEY, cls.crawler)
        logging.info('crawler saved into memcache.')
        return True
    @classmethod
    def get(cls):
        if cls.crawler: return cls.crawler
        # else try to get in memcache
        crawler = memcache.get(cls.CRAWLER_MEMCACHE_KEY)
        if crawler:
            cls.crawler = crawler
            return crawler
        # else create a new instance
        from Crawler import Crawler
        cls.crawler = Crawler(conf.DOMAIN)
        cls.store_in_memcache()
        return cls.crawler
    @classmethod
    def save(cls):
        cls.store_in_memcache()
        logging.info('crawler saved.')
        return True
        