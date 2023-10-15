import os
import sys
import random
from threading import Thread

from PySide6.QtGui import QTextCursor, QPalette, QColor

from handler.vosk_handler import to_wav
from ui.ui_main import Ui_MainWindow
from ui.ui_vosk_text import Ui_Form
from PySide6.QtGui import QIcon
from PySide6.QtCore import QThread, Signal, QStandardPaths
from PySide6.QtWidgets import (QApplication, QMainWindow, QMessageBox, QFileDialog, QWidget,
                               QVBoxLayout, )


def resource_path(relative_path):
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)


ico_path = resource_path("vtt.ico")


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.vosk_list = []
        self.setWindowIcon(QIcon(ico_path))


class WidgetText(QWidget, Thread):
    text_append_signal = Signal(str)

    def __init__(self, file_path):
        super().__init__()
        self.text_box = None
        suffix = file_path.split("/")[-1]
        self.path_name = suffix
        self.setGeometry(random.randint(50, 300), random.randint(50, 300), 50, 50)
        self.file_path = file_path
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.setWindowTitle(suffix)
        self.setWindowIcon(QIcon(ico_path))
        layout = QVBoxLayout()
        self.setLayout(layout)
        layout.addWidget(self.ui.content_text)

    def closeEvent(self, event) -> None:
        mainW.vosk_list.remove(self)

    def titleChange(self,newTitle):
        self.setWindowTitle(newTitle)
    def run(self):
        palette = self.ui.content_text.palette()
        palette.setColor(QPalette.Base, QColor("#fcfdfa"))  # 设置背景色
        self.ui.content_text.setPalette(palette)
        self.ui.content_text.setReadOnly(True)
        to_wav(self, self.file_path)
        self.ui.content_text.setReadOnly(False)


app = QApplication(sys.argv)
# 初始化窗口
mainW = MainWindow()
mainW.setWindowTitle("语音转文字")
mainW.setFixedSize(mainW.width(), mainW.height())
ui = mainW.ui


def event_confirm():
    ui.start_bt.clicked.connect(vosk_recognition)
    ui.file_path.mousePressEvent = file_path_mouse_event
    ui.file_path.returnPressed.connect(file_select)


def file_path_mouse_event(event):
    file_select()


def file_select():
    """ 获取桌面地址 """
    desktop_location = QStandardPaths.standardLocations(QStandardPaths.DesktopLocation)[0]
    file_name_path, types = QFileDialog.getOpenFileName(None, "选择音频文件", desktop_location)
    ui.file_path.setText(file_name_path)


def vosk_recognition():
    if ui.file_path.text() is None or ui.file_path.text().strip() == "":
        warning("警告", "请选择文件")
    else:
        ui_form = WidgetText(ui.file_path.text())
        mainW.vosk_list.append(ui_form)
        ui_form.show()
        ui_form.titleChange(ui_form.path_name + "（读取中）")
        ui_form.start()


def warning(title, content):
    msg = QMessageBox(text=content)
    msg.setWindowTitle(title)
    msg.setStandardButtons(QMessageBox.StandardButton.Ok)
    msg.exec_()


def main():
    event_confirm()
    mainW.show()
    sys.exit(app.exec_())
