# encoding: utf-8
from google.appengine.ext import webapp
from google.appengine.api import memcache
from google.appengine.ext.webapp.util import run_wsgi_app
import logging
import time
import conf
from db import CrawlerManager
from task import TaskManager
class StartHandler(webapp.RequestHandler):
    def get(self):
        TaskManager.add_crawler_task()
class CrawlHandler(webapp.RequestHandler):
    def get(self):
        start_time = time.time()
        crawler = CrawlerManager.get()
        logging.info(crawler)
        try:
            while time.time() - start_time < conf.MAX_TASK_TIME:
                if crawler.crawl_next() in ['pop url error',]: break
            crawler.log_current()
        except Exception, ex:
            logging.warn(ex)
        finally:
            # must be saved!
            CrawlerManager.save()
            #TaskManager.add_crawler_task()
app = webapp.WSGIApplication([
    ('/start', StartHandler),
    ('/crawl', CrawlHandler),
    ], debug=True)
def main():
    run_wsgi_app(app)
if __name__ == "__main__":
    main()