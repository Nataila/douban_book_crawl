#!/usr/bin/env python
# coding: utf-8
# cc @ 2017-09-18

from settings import MONGO_CLIENT

db = MONGO_CLIENT['proxy']


def get_proxy():
    proxies = {'https': ''}
    # record = db.proxy_data.find_one({'protocol': 'HTTPS'})
    record = db.proxy_data.aggregate([{'$sample': {'size': 1}}]).next()
    ip = 'https://%s:%s' % (record['ip'], record['port'])
    proxies['https'] = ip
    return proxies
