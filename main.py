import sys

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication

from login.LoginWindow import LoginMainWindow

if __name__ == '__main__':
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)  # 设置不同分辨率屏幕自适应
    app = QApplication(sys.argv)
    win = LoginMainWindow()
    sys.exit(app.exec_())