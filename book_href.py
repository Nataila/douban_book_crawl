#!/usr/bin/env python
# coding: utf-8
# cc @ 2017-09-18


import time
import requests
from bs4 import BeautifulSoup as BS

from proxy import get_proxy
import settings
r = settings.REDIS_CONNECT


class Crawl():
    """
    获取每本书的链接,写入Redis
    """
    def __init__(self):
        self.index_url = settings.DOUBAN_URL
        self.proxies = get_proxy()

    def get_book_url(self, start_url=None):
        if settings.SLEEP:
            time.sleep(settings.SLEEP)
        tag_url = start_url if start_url else r.rpop('tag_href')
        tag_books_url = '%s%s' % (self.index_url, tag_url)
        params = {'timeout': settings.TIME_OUT}
        if settings.USE_PROXY:
            params['proxies'] = self.proxies
        try:
            html = requests.get(tag_books_url, **params)
            soup = BS(html.content, 'xml')
            books_dom = soup.select('h2 > a')
            for b in books_dom:
                book_href = b.get('href')
                print 'book name: %s, href: %s' % (b.get('title'), book_href)
                r.lpush('book_href', book_href)

            # 下一页
            next_page = soup.select('link[rel="next"]')
            if next_page:
                start_url = next_page[0].get('href')
                return self.get_book_url(start_url)

            # redis 里面是否还有没完成任务
            tags_len = r.llen('tag_href')
            if tags_len:
                return self.get_book_url()

        except Exception as e:
            # timeout 重新写入队列
            # r.lpush('tag_href', tag_url)
            print e
            print 'retrying ...'
            self.proxies = get_proxy()
            self.get_book_url(tag_url)


craw = Crawl()
craw.get_book_url()
