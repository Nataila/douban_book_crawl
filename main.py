#!/usr/bin/env python
# coding: utf-8
# cc @ 2017-09-18

import requests
from bs4 import BeautifulSoup as BS

from proxy import get_proxy
import settings
r = settings.REDIS_CONNECT


class Crawl():
    def __init__(self):
        self.index_url = 'https://book.douban.com/'
        self.all_tags_url = 'https://book.douban.com/tag/'

    def get_all_tags(self):
        """
        获取所有的标签
        """
        try:
            proxies = get_proxy() if settings.USE_PROXY else {}
            html = requests.get(self.all_tags_url, proxies=proxies,
                                timeout=settings.TIME_OUT)
        except Exception as e:
            print e
            print 'retrying ...'
            return self.get_all_tags()
        soup = BS(html.content, 'xml')
        tags_dom_list = soup('a', 'tag-title-wrapper')
        for tag_dom in tags_dom_list:
            second_tags = tag_dom.find_next_sibling().find_all('a')
            for a in second_tags:
                tag_href = a.get('href')
                print 'get tag href: %s' % tag_href
                r.lpush('tag_href', tag_href)


craw = Crawl()
craw.get_all_tags()
