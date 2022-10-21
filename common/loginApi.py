import json
import os.path

import requests
from urllib.parse import urlparse

# 提取两个信息：
# 1、获取用于表示具体服务的: cookie_session_id
# 2、票据标识: my_client_ticket
from common import rwFile


def getCookieInfo():
    url = "http://lib-ic.scnu.edu.cn/clientweb/m/ic2/default.aspx"
    ticket = "";
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36 Edg/106.0.1370.37"
    }
    while True:
        res = requests.get(url=url, headers=headers, allow_redirects=False)
        # 状态码
        status = res.status_code
        # 响应头
        resHeaders = res.headers

        # 遍历所有响应头部的value信息
        ticket = res.cookies.get("my_client_ticket", ticket)
        # for value in resHeaders.values():
        #     # 提取出 my_client_ticket
        #     if value.find("my_client_ticket") != -1:
        #         ticket = value[value.index('=') + 1:value.index(';')]

        # 如果是重定向，则拼接出新的url
        if status == 302:
            if resHeaders['Location'][0] == '/':
                # 域名
                domain = urlparse(url).netloc
                # 协议
                scheme = urlparse(url).scheme
                url = scheme + "://" + domain + resHeaders['Location'];
            else:
                url = resHeaders['Location']
        else:
            break
    jsessionid = url[url.index('=') + 1:]
    cookieInfo = {"ticket": ticket, "jsessionid": jsessionid}
    print("cookie_session_id、my_client_ticket获取成功")
    return cookieInfo;


# 通过用户名和密码注册上面这个服务id，以方便后面使用到
def register(username, password, cookieInfo):
    url = "https://sso.scnu.edu.cn/AccountService/user/login.html"

    params = {
        "account": username,
        "password": password
    }
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36 Edg/106.0.1370.37"
    }
    cookie = {
        "cookie_session_id": cookieInfo["jsessionid"],
        "my_client_ticket": cookieInfo["ticket"]
    }
    # 发起验证
    res = requests.post(url=url, data=params, headers=headers, cookies=cookie, allow_redirects=False)
    if res.status_code == 200:
        return False

    # 验证通过后就会重定向
    url = res.headers['Location']
    res = requests.post(url=url, data=params, headers=headers, cookies=cookie, allow_redirects=False)
    print("cookie_session_id注册成功")
    return True


def getSessionId(cookieInfo):
    url = "https://sso.scnu.edu.cn/AccountService/openapi/onekeyapp.html?app_id=107"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36 Edg/106.0.1370.37"
    }

    cookie = {
        "cookie_session_id": cookieInfo["jsessionid"],
        "my_client_ticket": cookieInfo["ticket"]
    }
    res = requests.post(url=url, headers=headers, cookies=cookie)
    Session = res.cookies.get("ASP.NET_SessionId")
    print("my_client_ticket注册成功，ASP.NET_SessionId获取成功")
    return Session


def getToken(cookieInfo):
    url = "https://sso.scnu.edu.cn/AccountService/openapi/onekeyapp.html?app_id=97"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36 Edg/106.0.1370.37"
    }

    cookie = {
        "cookie_session_id": cookieInfo["jsessionid"],
        "my_client_ticket": cookieInfo["ticket"]
    }
    str = ""
    while(True):
        try:
            res = requests.post(url=url, headers=headers, cookies=cookie)
            str = res.text
            token = json.loads(str[str.index("{"):str.index("}") + 1])['token'];
            print("Token获取成功")
            return token
        except Exception as e:
            print(e)
            print(str.text)


def isAvailable(cookieInfo):
    url = "http://lib-ic.scnu.edu.cn/ClientWeb/pro/ajax/login.aspx?act=is_login"

    headers = {
        "Cookie": "my_client_ticket=%s; ASP.NET_SessionId=%s;" % (cookieInfo["ticket"], cookieInfo["sessionId"]),
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36 Edg/106.0.1370.37"
    }
    res = requests.get(url=url, headers=headers, allow_redirects=False)
    state = res.status_code

    if state == 200:
        print("直接使用上一次的登录凭证")
        return True
    else:
        print(res.status_code)
        print(res.text)
        print("开始自动登录")
        return False


def startLogin(username, password):
    print("==========开始获取身份凭证=============")
    if os.path.exists('../user.dat'):
        # 先直接从文件中读取，并且检验是否有效
        cookieInfo = rwFile.read()
        print(cookieInfo)
        # 满足以下四个条件才能用
        if cookieInfo is not None and \
                username == cookieInfo['username'] and \
                password == cookieInfo['password'] and \
                isAvailable(cookieInfo):
            print("直接使用上次的登录凭证")
            return cookieInfo

    # 开始准备登录
    cookieInfo = getCookieInfo()
    # 开始登录
    if not register(username, password, cookieInfo):
        return None
    # 获取凭据
    cookieInfo['sessionId'] = getSessionId(cookieInfo)
    # 获取token
    cookieInfo['token'] = getToken(cookieInfo)
    print("==========身份凭证获取成功=============")

    return cookieInfo
