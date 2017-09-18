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

TIME_OUT = 3
