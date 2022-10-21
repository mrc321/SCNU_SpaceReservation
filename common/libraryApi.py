import time
from datetime import datetime

import requests

# 需要新增两个参数id 和 pwd
def login(cookie):
    url = "http://lib-ic.scnu.edu.cn/ClientWeb/pro/ajax/login.aspx"
    params = {
        "act": "login",
        "id": '',
        "pwd": '',
        "role": 512
    }
    headers = {
        "Cookie": "my_client_ticket=%s; ASP.NET_SessionId=%s" % (cookie["ticket"], cookie["sessionId"]),
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36 Edg/106.0.1370.37"
    }
    res = requests.get(url=url, params=params, headers=headers)
    res.encoding = 'utf-8'
    return res.json()


def isArriveTime(specialTime):
    specialDateTime = time.strftime("%Y-%m-%d") + " " + specialTime
    specialTimeStamp = int(time.mktime(time.strptime(specialDateTime, '%Y-%m-%d %H:%M:%S')))
    nowTimeStamp = int(time.time())

    if specialTimeStamp - nowTimeStamp <= 0:
        return True
    else:
        return False


# 新版本
def reserve(reserveInfo, cookie):
    info = reserveInfo["data"]
    url = "http://lib-ic.scnu.edu.cn/ClientWeb/pro/ajax/reserve.aspx"

    params = {
        "dev_id": info['dev_id'],
        "lab_id": info['lab_id'],
        "room_id": info['room_id'],
        "kind_id": info['kind_id'],
        "type": "dev",
        "classkind": 1,
        "start": reserveInfo["liveDate"] + " " + reserveInfo["startTime"],
        "end": reserveInfo["liveDate"] + " " + reserveInfo["endTime"],
        "memo": "学习使用",
        "act": "set_resv"
    }
    headers = {
        "Cookie": "my_client_ticket=%s; ASP.NET_SessionId=%s" % (cookie["ticket"], cookie["sessionId"]),
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36 Edg/106.0.1370.37"
    }
    res = requests.get(url=url, params=params, headers=headers)
    res.encoding = 'utf-8'
    with open('t.html', 'w', encoding='utf-8') as f:
        f.write(res.text)
    return res.json()


def startReserve(reserveInfos, cookie, log):
    flag = True
    sleepTime = 60

    while (True):

        if flag & isArriveTime("19:55:00"):
            sleepTime = 1;
            flag = False

        for reserveInfo in reserveInfos:
            nowTime = datetime.now().strftime("%H:%M:%S")

            result = reserve(reserveInfo, cookie)

            if result['ret'] == -1:
                # print(result['msg'])
                loginResult = login(cookie)
                if loginResult['ret'] == 1:
                    log.emit("登录成功")
                else:
                    log.emit("登录失败")
                    log.emit(loginResult['msg'])
            elif result['ret'] == 1:
                log.emit(reserveInfo['name'] + "预约成功")
                return True
            else:
                log.emit(nowTime + " ----- " + reserveInfo['name'] + " " + result['msg'])
                time.sleep(sleepTime)


def multipleReserve(reserveInfos, cookie, log):
    for reserveInfo in reserveInfos:
        if reserveInfo["name"] == "研修室一":
            reserveInfo["data"] = {
                "dev_id": 100455558,
                "lab_id": 100455305,
                "room_id": 100455557,
                "kind_id": 100456486,
            }
        elif reserveInfo["name"] == "研修室二":
            reserveInfo["data"] = {
                "dev_id": 100455562,
                "lab_id": 100455305,
                "room_id": 100455561,
                "kind_id": 100456486,
            }
        elif reserveInfo["name"] == "研修室三":
            reserveInfo["data"] = {
                "dev_id": 100455570,
                "lab_id": 100455305,
                "room_id": 100455569,
                "kind_id": 100456486,
            }
        elif reserveInfo["name"] == "研修室四":
            reserveInfo["data"] = {
                "dev_id": 100455566,
                "lab_id": 100455305,
                "room_id": 100455565,
                "kind_id": 100456486,
            }
        elif reserveInfo["name"] == "LIB_03":
            reserveInfo["data"] = {
                "dev_id": 103347084,
                "lab_id": 103299342,
                "room_id": 103347083,
                "kind_id": 103315809,
            }
        elif reserveInfo["name"] == "LIB_02":
            reserveInfo["data"] = {
                "dev_id": 103346719,
                "lab_id": 103299342,
                "room_id": 103346718,
                "kind_id": 103315807,
            }
        elif reserveInfo["name"] == "LIB_05":
            reserveInfo["data"] = {
                "dev_id": 103346720,
                "lab_id": 103299342,
                "room_id": 103346718,
                "kind_id": 103315807,
            }
    return startReserve(reserveInfos, cookie, log)
