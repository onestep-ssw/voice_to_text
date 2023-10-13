import sys
from main import to_wav2
from ui.ui_main import Ui_MainWindow
from ui.ui_vosk_text import Ui_Form
from PySide6.QtGui import QTextCursor, QIcon
from PySide6.QtWidgets import (QApplication, QMainWindow, QMessageBox, QSystemTrayIcon, QMenu, QFileDialog, QWidget, QVBoxLayout)


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.vosk_list = []

class WidgetText(QWidget):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("My Widget")
        #self.setGeometry(100, 100, 300, 200)
        self.setGeometry(100, 100, 50, 50)
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        layout = QVBoxLayout()
        self.setLayout(layout)
        layout.addWidget(self.ui.content_text)


    def closeEvent(self, event) -> None:
        mainW.vosk_list.remove(self)



app = QApplication(sys.argv)
# 初始化窗口
mainW = MainWindow()
mainW.setFixedSize(mainW.width(), mainW.height())
ui = mainW.ui


def event_confirm():
    ui.start_bt.clicked.connect(vosk_recognition)
    ui.file_path.mousePressEvent = file_path_mouse_event
    ui.file_path.returnPressed.connect(file_select)


def file_path_mouse_event(event):
    print(event)
    file_select()


def file_select():
    file_name_path, types = QFileDialog.getOpenFileName()
    ui.file_path.setText(file_name_path)


def vosk_recognition():
    ui_form = WidgetText()
    mainW.vosk_list.append(ui_form)
    ui_form.show()
    to_wav2(ui_form.ui.content_text)




def main():
    event_confirm()
    mainW.show()
    sys.exit(app.exec_())
