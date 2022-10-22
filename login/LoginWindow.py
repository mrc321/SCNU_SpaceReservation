import os

from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtWidgets import QMainWindow, QMessageBox

from common import rwFile,loginApi
from login import LoginPage
from reserve.AppointmentWindow import AppointmentWindow


class LoginMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = LoginPage.Ui_MainWindow()
        self.ui.setupUi(self)
        # 准备好预约窗口
        self.afterWin = AppointmentWindow()

        self.style_init()
        self.login_button_init()
        self.input_init()
        self.show()



    def style_init(self):
        # 隐藏窗口
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)

        # 下面这四行是给左右两个界面和登录注册按钮加阴影的
        self.ui.label.setGraphicsEffect(QtWidgets.QGraphicsDropShadowEffect(blurRadius=25, xOffset=0, yOffset=0))
        self.ui.label_2.setGraphicsEffect(QtWidgets.QGraphicsDropShadowEffect(blurRadius=25, xOffset=0, yOffset=0))
        self.ui.login_button.setGraphicsEffect(QtWidgets.QGraphicsDropShadowEffect(blurRadius=25, xOffset=3, yOffset=3))

    # 登录按钮初始化
    def login_button_init(self):
        # 初始化登录按钮为禁用状态
        self.ui.login_button.setEnabled(False)
        # 给登录按钮绑定登录验证
        self.ui.login_button.clicked.connect(self.login_func)

    # 输入框初始化
    def input_init(self):
        # 自动填充以往的账号密码
        cookieInfo = rwFile.read()
        if cookieInfo is not None:
            self.ui.login_username_input.setText(cookieInfo['username'])
            self.ui.login_password_input.setText(cookieInfo['password'])
            self.ui.login_button.setEnabled(True)

        self.ui.login_username_input.textChanged.connect(self.check_input_func)
        self.ui.login_password_input.textChanged.connect(self.check_input_func)
        # 默认勾选
        self.ui.is_remember_checkbox.setChecked(True)

    # 检查输入是否有效
    def check_input_func(self):
        if self.ui.login_username_input.text() and self.ui.login_password_input.text():
            self.ui.login_button.setEnabled(True)
        else:
            self.ui.login_button.setEnabled(False)

    # 开始登录
    def login_func(self):
        username = self.ui.login_username_input.text()
        password = self.ui.login_password_input.text()

        cookieInfo = loginApi.startLogin(username, password)

        if cookieInfo is None:
            QMessageBox.critical(self, "提示信息", "账号或密码不正确！")
        else:
            # 如果选择记住，则将相关信息写入到文件
            if self.ui.is_remember_checkbox.isChecked():
                cookieInfo['username'] = username
                cookieInfo['password'] = password
                rwFile.write(cookieInfo)
            # QMessageBox.information(self, "提示信息", "登录成功！")
            # 切换窗口
            self.afterWin.login_success()
            self.close()



    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton and self.isMaximized() == False:
            self.m_flag = True
            self.m_Position = event.globalPos() - self.pos()  # 获取鼠标相对窗口的位置
            event.accept()
            self.setCursor(QtGui.QCursor(QtCore.Qt.OpenHandCursor))  # 更改鼠标图标

    def mouseMoveEvent(self, mouse_event):
        if QtCore.Qt.LeftButton and self.m_flag:
            self.move(mouse_event.globalPos() - self.m_Position)  # 更改窗口位置
            mouse_event.accept()

    def mouseReleaseEvent(self, mouse_event):
        self.m_flag = False
        self.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))



