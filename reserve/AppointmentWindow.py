import datetime
import sys
from time import sleep

from PyQt5 import QtCore, QtWidgets, QtGui

from reserve import ReservePage
from PyQt5.QtCore import Qt, QTime
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem

from common.TaskThread import LibraryThread


class AppointmentWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = ReservePage.Ui_AppointmentWindow()
        self.ui.setupUi(self)


    def login_success(self):
        self.libraryThread = LibraryThread()
        self.libraryThread.logSignal.connect(self.set_library_log_func)

        self.style_init()
        self.input_init()
        self.button_init()
        self.record_table_init()
        self.show()

    def style_init(self):
        # 隐藏窗口
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)

        self.ui.centralwidget.setGraphicsEffect(
            QtWidgets.QGraphicsDropShadowEffect(blurRadius=25, xOffset=3, yOffset=3))

        self.ui.start_library_button.setGraphicsEffect(
            QtWidgets.QGraphicsDropShadowEffect(blurRadius=25, xOffset=3, yOffset=3))
        self.ui.start_weige_button.setGraphicsEffect(
            QtWidgets.QGraphicsDropShadowEffect(blurRadius=25, xOffset=3, yOffset=3))

    def input_init(self):
        # 预约日期
        after_tomorrow_day = str((datetime.datetime.now() + datetime.timedelta(days=2)).strftime('%Y/%m/%d'))

        self.ui.reserve1_data_label.setText(after_tomorrow_day)
        self.ui.reserve2_data_label.setText(after_tomorrow_day)

        # 空间名称
        self.ui.library_room_list.addItems(['研修室一', '研修室二', '研修室三', '研修室四', 'LIB_03', 'LIB_02', 'LIB_05'])
        self.ui.weige_room_list.addItems(['实训室一', '实训室二', '实训室三', '实训室四', '实训室五', '实训室六', '实训室七', '实训室八'])

        # 开始时间默认为8:00
        self.ui.library_start_time.setTime(QTime(8, 0))

        # 结束时间默认为21:50
        self.ui.library_end_time.setTime(QTime(21, 50))

        # 维格的时间表list
        self.ui.weige_time_quantum.addItems(["08:10-9:00-09:10-10:00", "10:10-11:00", "11:10-12:00",
                                             "13:10-14:00", "14:10-15:00", "15:10-16:00", "16:10-17:30", "18:30-19:20",
                                             "19:30-20:20", "20:30-21:50"])

    def button_init(self):
        # 图书馆添加记录按钮绑定
        self.ui.library_add_button.clicked.connect(self.add_library_func)
        # 微格添加记录按钮时间绑定
        self.ui.weige_add_button.clicked.connect(self.add_weige_func)

        self.ui.start_library_button.clicked.connect(self.start_reserve_library)

        self.ui.start_weige_button.clicked.connect(self.start_reserve_weige)

    def record_table_init(self):
        # 为记录表绑定点击时间
        self.ui.record_table.clicked.connect(self.remove_row_func)

    # 删除指定行
    def remove_row_func(self):
        remove_row = self.ui.record_table.currentItem()
        if remove_row.text() == '删除':
            row_num = remove_row.row()
            self.ui.record_table.removeRow(row_num)

    # 图书馆按钮添加记录
    def add_library_func(self):
        row = self.ui.record_table.rowCount()
        self.ui.record_table.setRowCount(row + 1)

        # 添加记录前先检查一下时间的分钟是否为整10数,向下取整
        self.ui.library_start_time.setTime(
            QTime(self.ui.library_start_time.time().hour(), self.ui.library_start_time.time().minute() // 10 * 10))
        self.ui.library_end_time.setTime(
            QTime(self.ui.library_end_time.time().hour(), self.ui.library_end_time.time().minute() // 10 * 10))

        self.ui.record_table.setItem(row, 0, self.getTableItem(self.ui.reserve1_data_label.text()))
        self.ui.record_table.setItem(row, 1, self.getTableItem(self.ui.library_room_list.currentText()))
        self.ui.record_table.setItem(row, 2, self.getTableItem(self.ui.library_start_time.text()))
        self.ui.record_table.setItem(row, 3, self.getTableItem(self.ui.library_end_time.text()))
        self.ui.record_table.setItem(row, 4, self.getTableItem('删除'))

    # 微格按钮添加记录
    def add_weige_func(self):

        row = self.ui.record_table.rowCount()
        self.ui.record_table.setRowCount(row + 1)

        start_end_time = self.ui.weige_time_quantum.currentText().split('-')

        self.ui.record_table.setItem(row, 0, self.getTableItem(self.ui.reserve2_data_label.text()))
        self.ui.record_table.setItem(row, 1, self.getTableItem(self.ui.weige_room_list.currentText()))
        self.ui.record_table.setItem(row, 2, self.getTableItem(start_end_time[0]))
        self.ui.record_table.setItem(row, 3, self.getTableItem(start_end_time[1]))
        self.ui.record_table.setItem(row, 4, self.getTableItem('删除'))

    def set_library_log_func(self, log):
        self.ui.library_log.append(log)

    def set_weige_log_func(self, log):
        self.ui.weige_log.append(log)

    def start_reserve_library(self):
        self.libraryThread.start()

    def start_reserve_weige(self):
        sleep(10)

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

    def getTableItem(self, text):
        item = QTableWidgetItem(text)
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        return item




if __name__ == '__main__':
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    app = QApplication(sys.argv)
    win = AppointmentWindow()
    sys.exit(app.exec_())
