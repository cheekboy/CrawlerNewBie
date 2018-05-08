#!/usr/bin/python
# -*- coding:utf-8 -*-
import ssl
from urllib import parse, request


def getUserArtList(queryUserId):
    url = r'https://be02.bihu.com/bihube-pc/api/content/show/getUserArtList'
    headers = {
        'User-Agent': r'Mozilla/5.0 (Windows NT 10.0: Win64: x64)',
        'Content-Type': r'application/x-www-form-urlencoded;charset=utf-8',
        'Referer': r'https://bihu.com/people/' + str(queryUserId) + '/',
        'Connection': 'keep-alive',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,zh-TW;q=0.7',
    }
    data = {
        'queryUserId': queryUserId,
        'pageNum': 1
    }
    context = ssl._create_unverified_context()
    data = parse.urlencode(data).encode('utf-8')
    req = request.Request(url, headers=headers, data=data)
    rsp = request.urlopen(req, context=context).read()
    rsp = rsp.decode('utf-8')
    return rsp

if __name__ == "__main__":
    print(getUserArtList(13679))
