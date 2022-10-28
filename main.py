import random

from PyQt5 import QtWidgets, uic, QtCore, QtGui
from PyQt5.QtWidgets import QApplication, QMainWindow
import sys

if hasattr(QtCore.Qt, 'AA_EnableHighDpiScaling'):
    QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
if hasattr(QtCore.Qt, 'AA_UseHighDpiPixmaps'):
    QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)
colors = []
for i in range(18):
    colors.append("red")
for i in range(18):
    colors.append("black")
colors.append("green")


class StartWin(QMainWindow):
    def __init__(self):
        super(StartWin, self).__init__()
        uic.loadUi('start.ui', self)

        self.setWindowTitle("Рулетка")

        self.start1.clicked.connect(self.go)
        self.start1.setIcon(QtGui.QIcon('BtnImg.jpg'))
        self.start1.setIconSize(QtCore.QSize(1000, 1000))
        self.setWindowIcon(QtGui.QIcon('icon.png'))

    def go(self):
        self.menu_window = MenuWindow()
        self.menu_window.show()
        self.hide()


class MenuWindow(QMainWindow):
    def __init__(self):
        super(MenuWindow, self).__init__()
        uic.loadUi('goPlayMenu.ui', self)
        self.setWindowTitle("Рулетка")
        self.setWindowIcon(QtGui.QIcon('icon.png'))
        self.settingsBtn.clicked.connect(self.go_settings)
        self.goScoreBtn.clicked.connect(self.go_score)
        self.goPlayBtn.clicked.connect(self.go_play)

    def go_settings(self):
        self.settings_window = SettingsWindow()
        self.settings_window.show()
        self.hide()

    def go_score(self):
        self.score_window = ScoreWindow()
        self.score_window.show()
        self.hide()

    def go_play(self):
        self.play_window = PlayWindow()
        self.play_window.show()
        self.hide()


class SettingsWindow(QMainWindow):
    def __init__(self):
        super(SettingsWindow, self).__init__()
        uic.loadUi('SettingsWindow.ui', self)
        self.setWindowTitle("Рулетка")
        self.setWindowIcon(QtGui.QIcon('icon.png'))


class PlayWindow(QMainWindow):
    def __init__(self):
        super(PlayWindow, self).__init__()
        uic.loadUi('mainplay.ui', self)
        self.setWindowTitle("Рулетка")
        self.setWindowIcon(QtGui.QIcon('icon.png'))
        self.black_Btn.clicked.connect(self.set_black)
        self.green_btn.clicked.connect(self.set_green)
        self.red_Btn.clicked.connect(self.set_red)

    selected = ""

    def set_black(self):
        self.selected = "black"
        self.random_color()

    def set_green(self):
        self.selected = "green"
        self.random_color()

    def set_red(self):
        self.selected = "red"
        self.random_color()

    def random_color(self):
        if self.selected == random.choice(colors):
            self.label.setText("Вы выйграли!!!")
        else:
            self.label.setText("Вы проиграли!!!")


class ScoreWindow(QMainWindow):
    def __init__(self):
        super(ScoreWindow, self).__init__()
        uic.loadUi('RecordWindow.ui', self)
        self.setWindowTitle("Рулетка")
        self.setWindowIcon(QtGui.QIcon('icon.png'))


def application():
    app = QApplication(sys.argv)
    window = StartWin()

    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    application()
