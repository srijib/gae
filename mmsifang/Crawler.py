#-*- coding: utf-8 -*-
#!/usr/bin/env python
import re
import logging
from google.appengine.api import urlfetch
import conf
class Crawler:
    link_re = re.compile(r'<a.*?href\s*=\s*[\'"\s]*(.*?)(?:[\'">]|$)')
    img_re = re.compile(r'<img.*?src\s*=\s*[\'"\s]*(.*?)(?:[\'">]|$)')
    banned_suffix_list = ['.zip','.rar','.tar.gz','.doc','.docx','.pdf','.jpg','.gif','.png']
    banned_tag_list = ['javascript:', '#']
    def __init__(self, domain):
        if not domain.endswith('/'):
            domain = domain + '/'
        # make sure domain is with slash.
        self.domain = domain
        self.page_set = set()
        self.image_set = set()
        self.page_set.add(domain)
    def try_add_domain(self, link_url, current_url):
        if link_url.startswith('http'):
            return link_url
        # else (link_url without http, in local domain)
        if not self.domain in link_url:
            if link_url.startswith('/'):
                return '%s%s' %(self.domain, link_url[1:])
            else:
                return '%s/%s' %('/'.join(current_url.split('/')[:-1]), link_url)
        else:
            # very strange here
            return link_url
    def fetch_content(self, url):
        # Retry 3 times
        result = None
        for i in range(3):
            try:
                result = urlfetch.fetch(url)
                break
            except urlfetch.DownloadError, ex:
                logging.warn(ex)
        if result:
            return result.content
        else:
            return None
    def filter_links(self, link_url):
        # filter domains
        domain_allowed = False
        for tag in conf.ALLOWED_DOMAIN_TAGS:
            if tag in link_url:
                domain_allowed = True
                break
        if not domain_allowed:
            return False
        # filter big media files
        for suffix in self.banned_suffix_list:
            if link_url.lower().endswith(suffix): return False
        # filter tags in url
        for tag in self.banned_tag_list:
            if tag in link_url.lower(): return False
        # finally ok
        return True
    def get_page_links(self, html_content, current_url):
        links = self.link_re.findall(html_content)
        links = [self.try_add_domain(link, current_url) for link in links]
        links = filter(self.filter_links, links)
        return links
    def get_image_links(self, html_content, current_url):
        links = self.img_re.findall(html_content)
        links = [self.try_add_domain(link, current_url) for link in links]
        # links = filter(self.filter_links, links)
        return links
    def crawl_next(self):
        try:
            current_url = self.page_set.pop()
            self.page_set.add(current_url)
        except KeyError:
            logging.info('page_set is empty, maybe all done, or an error.')
            return 'pop url error'
        # else got next_url
        logging.info('fetching page: url("%s")' %current_url)
        html_content = self.fetch_content(current_url)
        if not html_content:
            logging.info('error: fetch_content function returns None')
            return 'fetch error'
        # else got html_content
        self.page_set.remove(current_url)
        page_links = self.get_page_links(html_content, current_url)
        image_links = self.get_image_links(html_content, current_url)
        self.page_set.update(page_links)
        # logging.info('added %d links, total %d links' %(len(page_links), len(self.page_set)))
        self.image_set.update(image_links)
        # logging.info('added %d images, total %d images' %(len(image_links), len(self.image_set)))
        return True
    def log_current(self):
        logging.info('total %d links, %d images' %(len(self.page_set), len(self.image_set)))