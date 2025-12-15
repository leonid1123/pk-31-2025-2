import pymysql
from PyQt6.QtWidgets import QLineEdit
from PyQt6.QtWidgets import QVBoxLayout
import sys
from pathlib import Path
from PyQt6.QtWidgets import QApplication, QWidget, \
QListWidget, QPushButton, QLabel
import pymysql.cursors

class Shop(QWidget):
    def __init__(self):
        super().__init__()
        self.id_list = []
        layout = QVBoxLayout()
        self.setLayout(layout)
        self.money = 1000
        self.money_lbl = QLabel("Денег:1000")
        layout.addWidget(self.money_lbl)
        self.main_lst = QListWidget()
        layout.addWidget(self.main_lst)
        self.main_lst.itemClicked.connect(self.sell_item)
        self.add_item_entry = QLineEdit()
        layout.addWidget(self.add_item_entry)
        self.add_btn = QPushButton("Добавить")
        layout.addWidget(self.add_btn)
        self.add_btn.clicked.connect(self.add_item)
        self.db_connect()
        self.get_all_items()
        self.show()

    def add_item(self):
        item = self.add_item_entry.text()
        sql = 'INSERT INTO items(name) VALUES(%s)'
        self.cur.execute(sql,(item,))
        self.conn.commit()
        self.money -= 100
        self.money_lbl.setText(f"Денег: {self.money}")
        self.get_all_items()

    def sell_item(self):
        item = self.main_lst.currentRow()
        id_to_delete = self.id_list[item]
        sql = "DELETE FROM items WHERE id=%s"
        self.cur.execute(sql, (id_to_delete,))
        self.conn.commit()
        self.get_all_items()
        self.money += 80
        self.money_lbl.setText(f"Денег: {self.money}")

    def db_connect(self):
        self.conn = pymysql.connect(
            host='localhost',
            user="pk31",
            password="1234",
            database='pk31_shop_test'
        )
        self.cur = self.conn.cursor()

    def get_all_items(self):
        sql = 'SELECT * FROM items'
        self.cur.execute(sql)
        ans = self.cur.fetchone()
        self.main_lst.clear()
        self.id_list.clear()
        while ans:
            txt = f"Название: {ans[1]}"
            self.main_lst.addItem(txt)
            self.id_list.append(ans[0])
            ans = self.cur.fetchone()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyleSheet(Path('login.qss').read_text(encoding='utf-8'))
    window = Shop()
    sys.exit(app.exec())