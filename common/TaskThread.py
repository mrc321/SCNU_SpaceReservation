from PyQt5.QtCore import QThread, pyqtSignal
import time


# 专门用来执行图书馆预约任务的主线程
from common import  loginApi,libraryApi


class LibraryThread(QThread):
    logSignal = pyqtSignal(str)  # 专门用来传输输出信息的信号

    def __init__(self):
        super(LibraryThread, self).__init__()
        self.is_on = True # 用来控制线程的关系

        self.reserveInfos = [{"liveDate": "2022-10-23", "name": "LIB_03", "startTime": "13:30", "endTime": "17:30"}]
        self.loginInfo = loginApi.startLogin("","")


    def run(self):
        print("开始运行图书馆预约线程")
        # 修改下面四个参数即可client_vpn_ticket=weeCnRGEC3Lo2Peb; ASP.NET_SessionId=xmjp1arbjsdjow453owbaz45; _d_id=708e05ea2dc2d3f76c093969ec857e
        cookie = {"ticket": self.loginInfo['ticket'],
                  "sessionId": self.loginInfo['sessionId']}
        libraryApi.multipleReserve(self.reserveInfos, cookie,self.logSignal)

