# encoding: utf-8
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
import logging
import conf
def calc_block_number(size):
    if size % conf.BLOCK_SIZE == 0:
        block_number = size / conf.BLOCK_SIZE
    else:
        block_number = size / conf.BLOCK_SIZE + 1
    return block_number
class ListHandler(webapp.RequestHandler):
    def get(self):
        from google.appengine.api import users
        from google.appengine.ext import db
        from google.appengine.ext.webapp import template
        template_values = {}
        from model import File
        downloader = users.get_current_user()
        query = db.GqlQuery("SELECT * FROM File WHERE downloader = :1", downloader)
        filelist = [item for item in query]
        for item in filelist:
            query = db.GqlQuery("SELECT * FROM FileBlock WHERE file = :1", item.key())
            downloaded_blocks = query.count()
            total_blocks = calc_block_number(item.size)
            item.percent = '%.0f%%(%d/%d)' %(float(downloaded_blocks)/total_blocks*100, downloaded_blocks, total_blocks)
        template_values['filelist'] = filelist
        template_values['logout_url'] = users.create_logout_url("")
        template_values['change_user_url'] = users.create_logout_url("list")
        template_values['nickname'] = downloader.nickname()
        self.response.out.write(template.render('templates/list.html', template_values))
        #for item in query:
        #    self.response.out.write("%s %s %d %s %d %s\n" %(item.name, str(item.url), item.size, item.mimetype, item.status, str(item.add_time)))
class AddDownloadHandler(webapp.RequestHandler):
    def check_exist_and_sustainable(self, url):
        import urllib2
        try:
            request = urllib2.Request(url = url)
            request.add_header('Range', 'bytes=0-0')
            result = urllib2.urlopen(request)
        except:
            return None
        # else successfully fetched
        if result.code == 206:
            filename = ''
            size = -1
            mimetype = ''
            if result.headers.dict.has_key('content-range'):
                str_range = result.headers.dict['content-range']
                try:
                    size = int(str_range.split('/')[-1])
                except: pass
            if result.headers.dict.has_key('content-disposition'):
                str_disposition = result.headers.dict['content-disposition']
                try:
                    str_filename = str_disposition.split('filename=')[-1]
                    filename = ''.join(str_filename.split('"'))
                except: pass
            else:
                import urlparse, os
                try:
                    filename = os.path.basename(urlparse.urlparse(url).path)
                except: pass
            if result.headers.dict.has_key('content-type'):
                mimetype = result.headers.dict['content-type']
            return (filename, size, mimetype)
        else:
            return False
    def get(self):
        url = self.request.get("url")
        if not url:
            self.response.out.write("download?url=file_url")
            return
        mixed_result = self.check_exist_and_sustainable(url)
        if mixed_result == None:
            self.response.out.write('error: url resource not found, or network error.')
            return
        if mixed_result == False:
            self.response.out.write('error: url resource cannot support continually download.')
            # todo small file download
            return
        # else result is a size
        try:
            filename, size, mimetype = mixed_result
        except:
            self.response.out.write('internal error: function "check_exist_and_sustainable" returned %s.' %str(mixed_result))
            return
        # got file size
        if size > 500*1024*1024:
            self.response.out.write('要下载的文件太大了(超过500MB),单个app承受不起啊(每天就1G流量..),正在计划搭建下载均衡器,请关注.<br><a href="list">返回</a>')
            return
        # calculate block_number
        block_number = calc_block_number(size)
        # create file record
        from model import EStatus, File
        from google.appengine.api import users
        downloader = users.get_current_user()
        new_file = File.get_or_insert('%s-%s'%(downloader, url), name = filename, url = url, downloader = downloader, size = size, mimetype = mimetype, status = EStatus.DOWNLOADING)
        new_file.put()
        key = new_file.key()
        from google.appengine.api import taskqueue
        def add_task():
            # add task
            for n in range(block_number):
                if n == block_number - 1: last = 'true'
                else: last = ''
                try:
                    taskqueue.add(url='/downloadfileblock', queue_name=conf.DOWNLOAD_FILEBLOCK_QUEUE_NAME, method='GET', params={'url': url, 'key': key, 'n': n, 'last': last}, transactional=False)
                except taskqueue.TombstonedTaskError:
                    logging.warn('added a task which is already run, url: %s, block_num: %d' %(url, n))
                    # added a task with that exact name before which is already run
                    # executed task names are kept around for some time to prevent accidental duplicates
                    pass
        add_task()
        self.response.out.write('添加成功!<br><a href="list">返回</a>')
        echo = 'Added tasks into queue: "%s" and started downloading, url: %s' %(conf.DOWNLOAD_FILEBLOCK_QUEUE_NAME, url)
        logging.info(echo)
class DownloadFileBlockHandler(webapp.RequestHandler):
    def fetch_file_block(self, url, n, is_last):
        import urllib2
        start = conf.BLOCK_SIZE * n
        end = conf.BLOCK_SIZE * (n + 1) - 1
        request = urllib2.Request(url = url)
        if not is_last:
            str_range = '%d-%d' %(start, end)
        else:
            str_range = '%d-' %(start,)
        request.add_header('Range', 'bytes=%s' %str_range)
        result = urllib2.urlopen(request)
        # successfully fetched
        str_info = 'url: %s, n: %d, is_last: %s' %(url, n, is_last)
        if result.code == 206:
            if not is_last:
                got_str_range = result.headers.dict['content-range']
                got_str_range = got_str_range.split('/')[0]
                got_str_range = got_str_range.split(' ')[-1]
                if got_str_range !=  str_range:
                    raise RuntimeError('Got content-range is not right, when fetching fileblock: %s' %str_info)
        else:
            raise RuntimeError('HTTP response code is %d, but respecting 206, when fetching fileblock: %s' %(result.code, str_info))
        # ok finally
        return result.read()
    def get(self):
        url = self.request.get('url')
        key = self.request.get('key')
        n = self.request.get('n')
        last = self.request.get('last')
        if not (url and key and n):
            self.response.out.write('url={url}&key={file_key}&n={block_number}&last={true|}')
            return
        # else ok
        # check aborted or not
        from google.appengine.api import memcache
        aborted_tasks = memcache.get(conf.ABORTED_TASKS_MEMCACHE_KEY) or set()
        if key in aborted_tasks:
            echo = 'Aborted task found, key:%s' %key
            logging.info(echo)
            self.response.out.write(echo)
            return
        if not last: is_last = False
        else: is_last = True
        n = int(n)
        block_content = self.fetch_file_block(url, n, is_last)
        logging.info("file block downloaded, url: %s, n: %d" %(url, n))
        from google.appengine.ext import db
        from model import FileBlock, File
        key_name = '%s - %d' %(url, n)
        new_file_block = FileBlock.get_or_insert(key_name, file = db.Key(key), n = n, content = db.Blob(block_content))
        logging.info("FileBlock saved with key_name: %s" %key_name)
class DeleteHandler(webapp.RequestHandler):
    def get(self):
        # todo
        # 1. when delete an task, firstly stop running it
        # 2. when delete an task, check key in memcache and also delete it
        from google.appengine.ext import db
        from model import File, FileBlock
        file_keys = self.request.get('file')
        if not file_keys:
            self.response.out.write('/delete?file={file_key1[,file_key2,...]}')
            return
        file_keys = file_keys.split(',')
        file_keys = [db.Key(key) for key in file_keys]
        block_keys = []
        for file_key in file_keys:
            arr_blocks = db.GqlQuery('select __key__ from FileBlock where file = :1', file_key).fetch(1000)
            block_keys += arr_blocks
        db.delete(file_keys)
        db.delete(block_keys)
        echo = '%d file task(s) deleted' %len(file_keys)
        self.response.out.write(echo)
        self.response.out.write('<br><a href="/list">返回</a>')
        logging.info(echo)
class StopHandler(webapp.RequestHandler):
    def get(self):
        # todo
        # 1. check key avilable
        # 2. when delete an task, check key in memcache and also delete it
        # 3. modify the file task state, and store it into db
        file_keys = self.request.get('file')
        if not file_keys:
            self.response.out.write('/stop?file={file_key1[,file_key2,...]}')
            return
        file_keys = file_keys.split(',')
        from google.appengine.api import memcache
        aborted_tasks = memcache.get(conf.ABORTED_TASKS_MEMCACHE_KEY)
        if not aborted_tasks:
            aborted_tasks = set()
        aborted_tasks.update(file_keys)
        memcache.set(conf.ABORTED_TASKS_MEMCACHE_KEY, aborted_tasks)
        echo = '%d file task(s) stopped' %len(file_keys)
        self.response.out.write(echo)
        self.response.out.write('<br><a href="/list">返回</a>')
        logging.info(echo)
class ResumeHandler(webapp.RequestHandler):
    def get(self):
        file_key = self.request.get('file')
        if not file_key:
            self.response.out.write('/resume?file={file_key}')
            return
        from google.appengine.api import users
        from google.appengine.api import memcache
        from google.appengine.api import taskqueue
        from google.appengine.ext import db
        from model import File
        aborted_tasks = memcache.get(conf.ABORTED_TASKS_MEMCACHE_KEY)
        if file_key in aborted_tasks:
            # remove aborted_tasks, or tasks cannot be done
            aborted_tasks.remove(file_key)
            memcache.set(conf.ABORTED_TASKS_MEMCACHE_KEY, aborted_tasks)
        downloader = users.get_current_user()
        obj_file_key = db.Key(file_key)
        obj_file = db.get(obj_file_key)
        query = db.GqlQuery("SELECT * FROM FileBlock WHERE file = :1", obj_file_key)
        downloaded_blocks = query.count()
        block_number = calc_block_number(obj_file.size)
        url = obj_file.url
        key = file_key
        def add_task():
            # add task
            for n in range(downloaded_blocks, block_number):
                if n == block_number - 1: last = 'true'
                else: last = ''
                try:
                    taskqueue.add(url='/downloadfileblock', queue_name=conf.DOWNLOAD_FILEBLOCK_QUEUE_NAME, method='GET', params={'url': url, 'key': key, 'n': n, 'last': last}, transactional=False)
                except taskqueue.TombstonedTaskError:
                    logging.warn('added a task which is already run, url: %s, block_num: %d' %(url, n))
                    # added a task with that exact name before which is already run
                    # executed task names are kept around for some time to prevent accidental duplicates
                    pass
        add_task()
        self.response.out.write('已继续任务<br><a href="list">返回</a>')
        echo = 'Resume block tasks into queue: "%s" and started downloading, url: %s' %(conf.DOWNLOAD_FILEBLOCK_QUEUE_NAME, url)
        logging.info(echo)
app = webapp.WSGIApplication([
    ('/list', ListHandler),
    ('/adddownload', AddDownloadHandler),
    ('/downloadfileblock', DownloadFileBlockHandler),
    ('/delete', DeleteHandler),
    ('/stop', StopHandler),
    ('/resume', ResumeHandler),
    ], debug=True)
def main():
    run_wsgi_app(app)
if __name__ == "__main__":
    main()