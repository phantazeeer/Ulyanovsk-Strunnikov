from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QTableWidgetItem
from PyQt5 import QtWidgets
from PyQt5 import uic
import sqlite3


class Window(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi("main.ui", self)
        self.tableWidget.setHorizontalHeaderLabels(["id", "name", "degree_of_roasting",
                                                    "ground/in_grains", "taste", "cost", "ammount"])
        self.pushButton.clicked.connect(self.show_table)
        self.con = sqlite3.connect("coffee.sqlite")
        self.pushButton_2.clicked.connect(self.go_redakt)

    def go_redakt(self):
        self.c = RefactorDB()
        self.c.show()
        self.con.close()
        self.hide()

    def show_table(self):
        cur = self.con.cursor()
        result = cur.execute(f"SELECT * FROM cofeyochek").fetchall()
        self.tableWidget.setRowCount(len(result))
        if not result:
            return
        self.tableWidget.setColumnCount(len(result[0]))
        for i, elem in enumerate(result):
            for j, val in enumerate(elem):
                self.tableWidget.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(val)))


class RefactorDB(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('addEditCoffeeForm.ui', self)
        self.setWindowTitle("Изменение данных")
        self.con = sqlite3.connect("coffee.sqlite")
        self.pushButton_2.clicked.connect(self.update_result)
        self.tableWidget.itemChanged.connect(self.item_changed)
        self.pushButton_3.clicked.connect(self.save_results)
        self.modified = {}
        self.titles = None
        self.update_all_result()
        self.pushButton_4.clicked.connect(self.return_to_main)
        self.tableWidget.setHorizontalHeaderLabels(["id", "name", "degree_of_roasting",
                                                    "ground/in_grains", "taste", "cost", "ammount"])

    def return_to_main(self):
        self.m = Window()
        self.m.show()
        self.con.close()
        self.hide()

    def update_all_result(self):
        cur = self.con.cursor()
        result = cur.execute(f"SELECT * FROM cofeyochek").fetchall()
        self.tableWidget_2.setRowCount(len(result))
        if not result:
            return
        self.tableWidget_2.setColumnCount(len(result[0]))
        self.titles = [description[0] for description in cur.description]
        for i, elem in enumerate(result):
            for j, val in enumerate(elem):
                self.tableWidget_2.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)
                self.tableWidget_2.setItem(i, j, QTableWidgetItem(str(val)))

    def update_result(self):
        cur = self.con.cursor()
        result = cur.execute("SELECT * FROM cofeyochek WHERE id=?",
                             (item_id := self.spinBox.text(),)).fetchall()
        self.tableWidget.setRowCount(len(result))
        if not result:
            self.statusBar().showMessage('Ничего не нашлось')
            return
        else:
            self.statusBar().showMessage(f"Нашлась запись с id = {item_id}")
        self.tableWidget.setColumnCount(len(result[0]))
        self.titles = [description[0] for description in cur.description]
        for i, elem in enumerate(result):
            for j, val in enumerate(elem):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(val)))
        self.modified = {}

    def item_changed(self, item):
        self.modified[self.titles[item.column()]] = item.text()

    def save_results(self):
        if self.modified:
            cur = self.con.cursor()
            que = "UPDATE cofeyochek SET\n"
            que += ", ".join([f"{key}='{self.modified.get(key)}'"
                              for key in self.modified.keys()])
            que += "WHERE id = ?"
            print(que)
            cur.execute(que, (self.spinBox.text(),))
            self.con.commit()
            self.modified.clear()
            self.update_all_result()


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    ex = Window()
    ex.show()
    sys.exit(app.exec())
