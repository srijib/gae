#-*- coding: utf-8 -*-
#!/usr/bin/env python

from google.appengine.ext import webapp
from google.appengine.ext.webapp import util
from google.appengine.ext import db
from google.appengine.api import urlfetch
from google.appengine.api import memcache
import re, zlib, time, marshal
from Models import *

class MainHandler(webapp.RequestHandler):
    # BBS Main Frame
    #__start_url = "http://bbs.sjtu.edu.cn/frame2.html"
    __start_url = "http://bbs.sjtu.edu.cn/php/bbsindex.html"
    __link_re = re.compile( r'<a.*?href\s*=\s*[\'"\s]*(.*?)(?:[\'">]|$)' )
    # <a.*?href\s*=\s*['"]?(.+?)(?:/?['">\s]|$)
    __prefix = "http://bbs.sjtu.edu.cn"
    __prefix_short = "bbs.sjtu.edu.cn"
    __banned_suffix_list = ['.zip','.rar','.tar.gz','.doc','.docx','.pdf','.jpg','.gif','.png']
    __TotalFetchPage = 50
    @classmethod
    def fetch_content(cls, url):
        # Retry 3 times
        result = None
        for i in range(3):
            try:
                result = urlfetch.fetch( url )
                break
            except:
                pass
        if result:
            if result.status_code == 200:
                return result.content
            else:
                return None
        else:
            return None
    @classmethod
    def get_links(cls, html_content):
        old_links = cls.__link_re.findall(html_content)
        links = []
        for link in old_links:
            try:
                link = link.decode("utf8")
            except:
                link = link.decode("GBK")
            file = False
            for suffix in cls.__banned_suffix_list:
                if link.endswith(suffix):
                    file = True
                    break
            if file:
                break
            if not cls.__prefix_short in link:
                if not "http" in link:
                    if link[0]=='/':
                        links.append("%s%s" %(cls.__prefix, link) )
                    else:
                        links.append("%s/%s" %(cls.__prefix, link) )
            else:
                links.append( link )
        return links
    def get(self):
        __debug = bool(self.request.get("debug"))
        if __debug: t = time.time()
        if SuperQueue.is_empty():
            SuperQueue.append(self.__start_url)
            SuperQueue.save()
        Dump.add(hash(self.__start_url))
        # Fetch
        for i in range(self.__TotalFetchPage):
            todo_url = SuperQueue.dequeue()
            if __debug: self.response.out.write('@fetch: <a href="%s">url</a>' %todo_url)
            html_content = self.fetch_content(todo_url)
            if html_content:
                new_page = Page(
                    url = todo_url,
                    indexded = False,
                    html = zlib.compress( html_content )
                    )
                new_page.put()
                links = self.get_links(html_content)
                for link in links:
                    link_hash = hash(link)
                    if __debug: self.response.out.write(' <a href="%s">H</a>' %link)
                    if not Dump.contains(link_hash):
                        Dump.add(link_hash)
                        SuperQueue.append(link)
                    else:
                        if __debug: self.response.out.write('r')
                        pass
                if __debug: self.response.out.write('<br>')
        SuperQueue.save()
        Dump.save()
        if __debug:
            self.response.out.write("<br>hash_list_dump size: %d<br>"%Dump.get_length())
            self.response.out.write(str(memcache.get_stats()))
            self.response.out.write('<br><br>')
            self.response.out.write("TOTAL TIME: %f seconds<br>" %(time.time() - t))
            self.response.out.write('<br><br>')
        self.response.out.write('%d Pages fetched.' %self.__TotalFetchPage)
def main():
    application = webapp.WSGIApplication([('/spider', MainHandler)],
                                         debug=True)
    util.run_wsgi_app(application)

if __name__ == '__main__':
    main()
