#!/usr/bin/env python
# coding: utf-8
# cc @ 2017-09-18

import redis
import pymongo

REDIS_CONNECT = redis.Redis(host='127.0.0.1', port=6379, db=10)

DOUBAN_URL = 'https://book.douban.com'

MONGO_HOST = '127.0.0.1'
MONGO_PORT = 27017

MONGO_CLIENT = pymongo.MongoClient(MONGO_HOST, MONGO_PORT)

TIME_OUT = 5

USE_PROXY = False

SLEEP = 1.5

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh,en;q=0.8,en-US;q=0.6,zh-CN;q=0.4,zh-TW;q=0.2',
    'Cookie': 'll="108288"; _ga=GA1.2.749289946.1429713374; bid=ccoUHJEI0bA; gr_user_id=a73b172e-9bc7-4dd9-98f6-6292241aa94f; ct=y; __ads_session=KIIYJ8GJ+QhPTqEMLgA=; ps=y; push_noty_num=0; push_doumail_num=0; as="https://book.douban.com/tag/%E5%B0%8F%E8%AF%B4"; ap=1; viewed="26963900_25862578_27090347"; gr_session_id_22c937bbd8ebd703f2d8e9445f7dfd03=ce73f6d9-c414-4ed0-a6a8-cf734d0f78bd; gr_cs1_ce73f6d9-c414-4ed0-a6a8-cf734d0f78bd=user_id%3A0; __utmt_douban=1; __utma=30149280.749289946.1429713374.1505793021.1505799495.55; __utmb=30149280.1.10.1505799495; __utmc=30149280; __utmz=30149280.1505787838.53.35.utmcsr=douban.com|utmccn=(referral)|utmcmd=referral|utmcct=/accounts/login; __utmv=30149280.11451; _vwo_uuid_v2=53F8C2E8272490FD47E2E92E2D162097|e6f37e430d58e0753d3c673ef7826a71'
}
