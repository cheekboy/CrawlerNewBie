#!/usr/bin/python
# -*- coding:utf-8 -*-
import json
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
    # rsp = request.urlopen(req).read()
    rsp = rsp.decode('utf-8')
    return rsp

def check_need_up(body):
    data_str=json.loads(body)
    res = data_str['res']
    need_up = False
    artId = 0
    is_succ = False
    log_content_format = '【%s】的最新文章已有【%d】赞，文章收益【¥%.2f】，文章标题【%s】'
    if res == 1 and data_str["data"]["total"] > 0:
        item=data_str["data"]['list'][0]
        log_content = log_content_format % (item['userName'], item['ups'], item['money'], item['title'])
        print(log_content)
        if item['up'] == 0 and item['ups'] < 100:
            need_up = True
        artId = item['id']

    if res==1:
        is_succ = True

    return is_succ, need_up, artId

if __name__ == "__main__":
    body = getUserArtList(13679)
    print (body)
    print(check_need_up(body))
