# encoding: utf-8
from google.appengine.api import taskqueue
import logging
class TaskManager:
    @staticmethod
    def add_crawler_task():
        taskqueue.add(url='/crawl', method='GET')
        logging.info('added a crawler task')