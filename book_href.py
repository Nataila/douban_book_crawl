#!/usr/bin/env python
# coding: utf-8
# cc @ 2017-09-18


# import time
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

    def get_book_url(self):
        tag_url = r.rpop('tag_href')
        tag_books_url = '%s%s' % (self.index_url, tag_url)
        try:
            html = requests.get(tag_books_url, proxies=self.proxies,
                                timeout=settings.TIME_OUT)
            soup = BS(html.content, 'xml')
            books_dom = soup.select('h2 > a')
            for b in books_dom:
                book_href = b.get('href')
                print 'book name: %s, href: %s' % (b.get('title'), book_href)
                r.lpush('book_href', book_href)

            # next_page = soup.select('.next > a')
            # redis 里面是否还有没完成任务
            tags_len = r.llen('tag_href')
            if tags_len:
                # time.sleep(3)
                return self.get_book_url()
        except Exception as e:
            # timeout 重新写入队列
            r.lpush('tag_href', tag_url)
            print e
            print 'retrying ...'
            self.proxies = get_proxy()
            self.get_book_url()


craw = Crawl()
craw.get_book_url()
