from PyQt5.QtWidgets import QApplication, QWidget, QTableWidgetItem
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


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    ex = Window()
    ex.show()
    sys.exit(app.exec())
