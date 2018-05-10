#!/usr/bin/python
# -*- coding:utf-8 -*-
import json
import ssl, time
from urllib import parse, request

ISOTIMEFORMAT = '%Y-%m-%d %X'


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
    data_str = json.loads(body)
    res = data_str['res']
    need_up = False
    artId = 0
    is_succ = False
    log_content_format = '[%s]—【%s】的最新文章已有【%d】赞，文章收益【¥%.2f】，文章标题【%s】'
    if res == 1 and data_str["data"]["total"] > 0:
        item = data_str["data"]['list'][0]
        log_content = log_content_format % (datetime_str(), item['userName'], item['ups'], item['money'],
        item['title'])
        print(log_content)
        if item['up'] == 0 and item['ups'] < 100:
            need_up = True
        artId = item['id']

    if res == 1:
        is_succ = True

    return is_succ, need_up, artId


def upVote(artId):
    url = r'https://be02.bihu.com/bihube-pc/api/content/upVote'
    headers = {
        'User-Agent': r'Mozilla/5.0 (iPhone; CPU iPhone OS 10_3 like Mac OS X) AppleWebKit/602.1.50 (KHTML, like Gecko) CriOS/56.0.2924.75 Mobile/14E5239e Safari/602.1',
        'Content-Type': r'application/x-www-form-urlencoded;charset=utf-8',
        'Referer': r'https://bihu.com/article/356754',
        'Origin': r'https://bihu.com',
        'Connection': 'keep-alive',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,zh-TW;q=0.7'
    }
    data = {
        'userId': config['userId'],
        'accessToken': config['accessToken'],
        'artId': artId
    }
    context = ssl._create_unverified_context()
    data = parse.urlencode(data).encode('utf-8')
    req = request.Request(url, headers=headers, data=data)
    rsp = request.urlopen(req, context=context).read()
    rsp = rsp.decode('utf-8')
    print("[点赞]-[返回]: " + rsp)

    return rsp


config = {
    'userId': '13679',
    'accessToken': '9644f6cc3c9f4c87944ed92fdfcbc0f5',
}

vip_list = [
    {'name': '金马', 'userId': 9909, 'latestArtTime': 0},
    {'name': '南宫远', 'userId': 2234, 'latestArtTime': 0},
    {'name': 'JIMI', 'userId': 12627, 'latestArtTime': 0},
    {'name': '玩火的猴子', 'userId': 483, 'latestArtTime': 0},
    {'name': 'cherry', 'userId': 30991, 'latestArtTime': 0},
    {'name': '区块佣兵', 'userId': 692, 'latestArtTime': 0},
    {'name': '爱思考的糖', 'userId': 1385, 'latestArtTime': 0},
    {'name': '钱串串', 'userId': 41279, 'latestArtTime': 0},
    {'name': '一休哥', 'userId': 197646, 'latestArtTime': 0},
]


def getFollowArtList():
    url = r'https://be02.bihu.com/bihube-pc/api/content/show/getFollowArtList'
    headers = {
        'User-Agent': r'Mozilla/5.0 (Windows NT 10.0: Win64: x64)',
        'Content-Type': r'application/x-www-form-urlencoded;charset=utf-8',
        'Referer': r'https://bihu.com/?category=follow',
        'Connection': 'keep-alive',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,zh-TW;q=0.7',
    }
    data = {
        'userId': config['userId'],
        'accessToken': config['accessToken'],
    }
    context = ssl._create_unverified_context()
    data = parse.urlencode(data).encode('utf-8')
    req = request.Request(url, headers=headers, data=data)
    rsp = request.urlopen(req, context=context).read()
    rsp = rsp.decode('utf-8')
    return rsp


def Run():
    isRunning = True
    while isRunning:
        body = getFollowArtList()
        succ = VoteFollowArtList(body)
        if succ:
            time.sleep(5)
        else:
            isRunning = False
            break


def datetime_str():
    return time.strftime(ISOTIMEFORMAT, time.localtime(time.time()))


def VoteFollowArtList(body):
    data_str = json.loads(body)
    res = data_str['res']

    log_content_format = '[$s]-【%s】的最新文章已有【%d】赞，文章收益【¥%.2f】，文章标题【%s】'
    if res == 1 and data_str["data"]["artList"]["size"] > 0:
        for item in data_str["data"]["artList"]["list"]:
            log_content = log_content_format % (datetime_str(), item['userName'], item['ups'], item['money'], item['title'])
            print(log_content)

            is_vip_art = False
            for vipItem in vip_list:
                if item['userId'] == vipItem['userId']:
                    is_vip_art = True
                    break

            if (is_vip_art):
                if item['up'] == 0 and item['ups'] < 100:
                    print(item)
                    upVote(item['id'])
    return res == 1

if __name__ == "__main__":
    # body = getUserArtList(13679)
    # print(body)
    # is_succ, need_up, artId = check_need_up(body)
    # if (need_up):
    #     upVote(artId)

    Run()
