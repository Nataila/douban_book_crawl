#!/usr/bin/env python
# coding: utf-8
# cc @ 2017-09-19

import time
import re
import argparse

import requests
from bs4 import BeautifulSoup as BS

from proxy import get_proxy
import settings
r = settings.REDIS_CONNECT


class Crawl():
    '''
    获取每本书的详情
    '''

    def __init__(self, use_proxy, timeout, sleep_time):
        print 'use proxy:%s, timeout: %s, sleep time: %s' % (
            use_proxy, timeout, sleep_time)
        self.use_proxy = use_proxy
        self.timeout = timeout
        self.sleep_time = sleep_time
        self.proxies = get_proxy()
        self.db = settings.MONGO_CLIENT['douban_book']

    def get_detail(self, url=None):
        if self.sleep_time:
            time.sleep(self.sleep_time)
        url = url if url else r.rpop('book_href')
        params = {
            'timeout': settings.TIME_OUT,
            'headers': settings.HEADERS
        }
        if self.use_proxy:
            params['proxies'] = self.proxies
        try:
            html = requests.get(url, **params)
            soup = BS(html.content, 'lxml')
            insert_data = {
                'name': soup.select_one('h1 span').text,
                'author': soup.select_one('#info a').text.replace(
                    '\n', '').replace(' ', ''),
                'db_grade': float(soup.find('strong').text.strip()),
                'db_id': re.search(r'\d+', url).group()
            }
            img_dom = soup.select_one('#mainpic img')
            if img_dom:
                insert_data['img'] = img_dom.get('src').split('/')[-1]
            info_map = {
                'pub_year': u'出版年',
                'page': u'页数',
                'price': u'定价',
                'isbn': u'ISBN:'
            }
            for info in info_map:
                span = soup.find('span', text=re.compile(info_map[info]))
                if span:
                    item_name = span.next_sibling.replace(
                        '\n', '').replace(' ', '')
                    insert_data[info] = item_name
            print insert_data.get('name')
            self.db.book.insert(insert_data)

            books_len = r.llen('book_href')
            if books_len:
                return self.get_detail()
        except Exception as e:
            print url
            print e
            print 'retrying ...'
            self.proxies = get_proxy()
            self.get_detail(url)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='manual to this script')
    parser.add_argument('--use-proxy', type=bool, default=settings.USE_PROXY)
    parser.add_argument('--time-out', type=int, default=settings.TIME_OUT)
    parser.add_argument('--sleep-time', type=int, default=settings.SLEEP)
    args = parser.parse_args()
    crawl = Crawl(args.use_proxy, args.time_out, args.sleep_time)
    crawl.get_detail()
