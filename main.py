import random
import sqlite3
from PyQt5 import QtWidgets, uic, QtCore, QtGui
from PyQt5.QtSql import QSqlDatabase, QSqlQuery
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QTableWidget
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

global money
global name
global record


class StartWin(QMainWindow):
    def __init__(self):
        super(StartWin, self).__init__()
        uic.loadUi('ui/start.ui', self)
        self.setWindowTitle("Рулетка")
        self.next_Btn.clicked.connect(self.go)
        self.setWindowIcon(QtGui.QIcon('res/icon.png'))
        global name
        name = self.enter_nick.text()

    # def dialog(self):
    #     uic.loadUi('ui/dialog.ui', self)
    #     self.setWindowTitle("Рулетка")
    #     self.setWindowIcon(QtGui.QIcon('res/icon.png'))
    #     self.yes_Btn.clicked.connect(self.obu)
    #     self.no_Btn.clicked.connect(self.go)

    # def imgui(self):
    #    uic.loadUi('ui/imgui.ui', self)
    #    self.img_Btn.clicked.connect(self.go)

    def go(self):
        global record
        con = sqlite3.connect("res/db.db")
        cur = con.cursor()
        cur.execute("SELECT name FROM players")
        if bool((cur.execute(
                f"""
                SELECT money FROM players WHERE name LIKE '{name}'""").fetchall())):
            global money
            money = (int(cur.execute(f"""
            SELECT money FROM players WHERE name LIKE '{name}'""").fetchall()[0][0]))
        else:
            cur.execute(f"""
            INSERT INTO players (
                        name
                    )
                    VALUES (
                        '{name}'
                        );
            """)
            cur.execute(f"""
            INSERT INTO records (name, record) VALUES ('{name}', '1000');
""")
            con.commit()
            money = (int(cur.execute(f"""
                        SELECT money FROM players WHERE name LIKE '{name}'""").fetchall()[0][0]))
        if bool(cur.execute(f"""
SELECT record FROM records WHERE name LIKE '{name}'""").fetchall()):
            record = int(cur.execute(f"SELECT record FROM records WHERE name LIKE '{name}'").fetchall()[0][0])
            con.commit()
        else:
            cur.execute(f"""INSERT INTO records (
                        name,
                        record
                    )
                    VALUES (
                        {name},
                        1000
                    );

""")
            record = int(cur.execute(f"SELECT record FROM records WHERE name LIKE '{name}'").fetchall()[0][0])
            con.commit()
        con.close()

        self.menu_window = MenuWindow()
        self.menu_window.show()
        self.hide()


class MenuWindow(QMainWindow):
    def __init__(self):
        super(MenuWindow, self).__init__()
        uic.loadUi('ui/goPlayMenu.ui', self)
        self.setWindowTitle("Рулетка")
        self.setWindowIcon(QtGui.QIcon('res/icon.png'))
        self.settingsBtn.clicked.connect(self.go_settings)
        self.goScoreBtn.clicked.connect(self.go_score)
        self.goPlayBtn.clicked.connect(self.go_play)
        self.money_count.setText(f"Деньги: {money}")

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
        uic.loadUi('ui/SettingsWindow.ui', self)
        self.setWindowTitle("Рулетка")
        self.setWindowIcon(QtGui.QIcon('res/icon.png'))


class PlayWindow(QMainWindow):
    def __init__(self):
        super(PlayWindow, self).__init__()
        uic.loadUi('ui/mainplay.ui', self)
        self.setWindowTitle("Рулетка")
        self.setWindowIcon(QtGui.QIcon('res/icon.png'))
        self.black_Btn.clicked.connect(self.set_black)
        self.green_Btn.clicked.connect(self.set_green)
        self.red_Btn.clicked.connect(self.set_red)
        self.back_Btn.clicked.connect(self.go_back)
        self.money_score.setText(f'Деньги: {money}')
        self.helpBtn.clicked.connect(self.obu)

    def obu(self):
        self.win = Obu()
        self.win.show()

    def go_back(self):
        self.menu_window = MenuWindow()
        self.menu_window.show()
        self.hide()

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
        global money
        global name

        if money >= int(self.bet_ent.toPlainText()) > 0:
            a = random.choice(colors)
            if self.selected == a:
                self.label.setText("Вы выйграли!!!")
                if a == "black":
                    self.label_2.setText("Выпавший цвет: черный")
                    money += int(self.bet_ent.toPlainText())
                if a == "red":
                    self.label_2.setText("Выпавший цвет: красный")
                    money += int(self.bet_ent.toPlainText())
                if a == "green":
                    self.label_2.setText("Выпавший цвет: зеленый")
                    money += int(self.bet_ent.toPlainText()) * 10
            else:
                self.label.setText("Вы проиграли!!!")
                money -= int(self.bet_ent.toPlainText())
                if a == "black":
                    self.label_2.setText("Выпавший цвет: черный")
                if a == "red":
                    self.label_2.setText("Выпавший цвет: красный")
                if a == "green":
                    self.label_2.setText("Выпавший цвет: зеленый")

        if money <= 0:
            money = 10
        con = sqlite3.connect("res/db.db")
        cur = con.cursor()
        cur.execute("SELECT name FROM players")
        con.execute(f"""
        UPDATE players
        SET money = {money}
        WHERE name = '{name}';
        """)
        con.commit()
        money = (int(cur.execute(f"""
                                SELECT money FROM players WHERE name LIKE '{name}'""").fetchall()[0][
                         0]))
        self.money_score.setText(f'Деньги: {money}')
        if money > record:
            con.execute(f"""
            UPDATE records
            SET record ={record}
            WHERE name = {name}""")


class Obu(QMainWindow):
    def __init__(self):
        super(Obu, self).__init__()
        uic.loadUi('ui/obu.ui', self)
        self.setWindowTitle("Рулетка")
        self.setWindowIcon(QtGui.QIcon('res/icon.png'))
        self.backobu_Btn.clicked.connect(self.go_back)

    def go_back(self):
        self.hide()


class ScoreWindow(QMainWindow):
    def __init__(self):
        super(ScoreWindow, self).__init__()
        uic.loadUi('ui/db_view.ui', self)
        self.setWindowTitle("Рулетка")
        self.setWindowIcon(QtGui.QIcon('res/icon.png'))
        self.con = QSqlDatabase.addDatabase("QSQLITE")
        self.con.setDatabaseName("res/db.db")
        self.con.open()
        self.db_view.setColumnCount(2)
        self.db_view.setHorizontalHeaderLabels(["Имя", "Рекорд"])
        self.back_Btn.clicked.connect(self.go_back)

        query = QSqlQuery("""
        SELECT name,
        record
        FROM [records];
        """)
        while query.next():
            rows = self.db_view.rowCount()
            self.db_view.setRowCount(rows + 1)
            self.db_view.setItem(rows, 0, QTableWidgetItem(str(query.value(0))))
            self.db_view.setItem(rows, 1, QTableWidgetItem(str(query.value(1))))
        self.db_view.resizeColumnsToContents()

    def go_back(self):
        self.menu_window = MenuWindow()
        self.menu_window.show()
        self.hide()


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


def application():
    app = QApplication(sys.argv)
    window = StartWin()
    sys.excepthook = except_hook
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    application()
