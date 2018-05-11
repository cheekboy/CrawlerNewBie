#!/usr/bin/env Python
# coding=utf-8
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
        # 'Accept-Encoding': 'gzip, deflate, br',
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
        # 'Accept-Encoding': 'gzip, deflate, br',
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
    'phone': '13818858215',
    'password': 'd13522a05fb837e5b5fe8457240f165f5f54ac449462c45dc1cebe94b1056510',
    'accessToken': '72e6f04d0f4940c1ab5bbba43fc5017d',
    'energy': 55,
    'energUpdateTime': 0
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
        # 'Accept-Encoding': 'gzip, deflate, br',
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
    succ = loginViaPassword()
    if not succ:
        print('很遗憾，登录失败了')
        return

    print('已成功登录，请开始你的表演。。。')
    print('你想给以下大V点赞。。。')
    print(vip_list)

    while succ:
        update_energy(0)
        if has_vote_energy():
            body = getFollowArtList()
            list_succ, vote_succ = VoteFollowArtList(body)
            if not list_succ:
                succ = False
                break
            elif vote_succ:
                print(':)点赞成功')
                time.sleep(5)
        else:
            print('当前能量不足了，稍后再试')
            time.sleep(10)

def datetime_str():
    return time.strftime(ISOTIMEFORMAT, time.localtime(time.time()))


def VoteFollowArtList(body):
    data_str = json.loads(body)
    res = data_str['res']

    vote_suc = False
    log_content_format = '[%s]-【%s】的最新文章已有【%d】赞，文章收益【¥%.2f】，文章标题【%s】'
    if res == 1 and data_str["data"]["artList"]["size"] > 0:
        for item in data_str["data"]["artList"]["list"]:
            log_content = log_content_format % (datetime_str(), item['userName'], int(item['ups']), item['money'], item['title'])
            print(log_content)

            is_vip_art = False
            for vipItem in vip_list:
                if item['userId'] == vipItem['userId']:
                    is_vip_art = True
                    break

            if (is_vip_art):
                if item['up'] == 0 and item['ups'] < 100:
                    print(item)
                    vote_suc = upVote(item['id'])
                    if vote_suc:
                        update_energy(10)
                        print(':)点赞成功，能量减少10')
    return res == 1, vote_suc


def parse_loginResult(body):
    data_str = json.loads(body)
    res = data_str['res']
    is_succ = False
    if res==1:
        config['userId'] = data_str['data']['userId']
        config['accessToken'] = data_str['data']['accessToken']
        is_succ = True
    return is_succ


def loginViaPassword():
    url = r'https://be02.bihu.com/bihube-pc/api/user/loginViaPassword'
    headers = {
        'User-Agent': r'Mozilla/5.0 (Windows NT 10.0: Win64: x64)',
        'Content-Type': r'application/x-www-form-urlencoded;charset=utf-8',
        'Referer': r'https://bihu.com/login',
        'Connection': 'keep-alive',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,zh-TW;q=0.7',
    }
    data = {
        'phone': config['phone'],
        'password': config['password']
    }
    context = ssl._create_unverified_context()
    data = parse.urlencode(data).encode('utf-8')
    req = request.Request(url, headers=headers, data=data)
    rsp = request.urlopen(req, context=context).read()
    rsp = rsp.decode('utf-8')
    # data_str = json.load(rsp)['data']
    print(rsp)

    is_succ = parse_loginResult(rsp)
    return is_succ

def has_vote_energy():
    return config['energy'] >= 10

def update_energy(consume):
    if config['energy'] == 100 and consume == 0:
        return;
    if config['energy'] < consume:
        return
    updateTime = time.time()
    newEnergy = (updateTime - config['energyUpdateTime']) * 100 / (24 * 60 * 60)
    config['energy'] = config['energy'] + newEnergy - consume
    if config['energy'] > 100:
        config['energy'] = 100
    config['energyUpdateTime'] = updateTime
    print(datetime_str() + '\t当前剩余能量：' + str(config['energy']))

if __name__ == "__main__":
    # body = getUserArtList(13679)
    # print(body)
    # is_succ, need_up, artId = check_need_up(body)
    # if (need_up):
    #     upVote(artId)
    config['energyUpdateTime'] = time.time()
    Run()
