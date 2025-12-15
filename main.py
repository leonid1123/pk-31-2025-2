'''
RPG - магазин и инвентарь
репозитарий: https://github.com/leonid1123/pk-31-2025-2
'''
import sys
from pathlib import Path
from PyQt6.QtWidgets import QApplication, QWidget, \
QListWidget, QGridLayout, QPushButton, QComboBox, QLabel
import pymysql.cursors

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.items_id_lst = []#id всех вещей
        self.inventory_items_id = []#id вещей в инвентаре
        self.shop_items_id = []#id вещей в магазине
        self.setWindowTitle("САМАЯ ЛУЧШАЯ РОЛЁВКА")
        layout = QGridLayout()
        self.setLayout(layout)
        self.db_connect()

        layout.addWidget(QLabel('Инвентарь'),0,0)
        layout.addWidget(QLabel('Добавление в инвентарь'),0,1)
        layout.addWidget(QLabel('Магазин'),0,2,1,2)

        self.inventory_lst = QListWidget()
        self.inventory_lst.setFixedWidth(500)
        self.shop_lst = QListWidget()
        self.shop_lst.setFixedWidth(500)
        self.sell_btn = QPushButton("Продать")
        self.sell_btn.clicked.connect(self.sel_item)
        self.buy_btn = QPushButton("Купить")
        self.buy_btn.clicked.connect(self.buy_item)
        self.all_items_lst = QComboBox()
        self.all_items_lst.activated.connect(self.add_inventory)

        layout.addWidget(self.inventory_lst,1,0)
        layout.addWidget(self.shop_lst,1,2,1,2)
        layout.addWidget(self.sell_btn,2,2)
        layout.addWidget(self.buy_btn,2,3)
        layout.addWidget(self.all_items_lst,1,1)
        self.get_shop()
        self.get_all_items()
        self.show_inventory()
        self.show()

    def db_connect(self):
        self.connection = pymysql.connect(
            host='localhost',
            user='pk31',
            password='1234',
            database='pk31_rpg'
        )
        self.cursor = self.connection.cursor()

    def get_shop(self):
        sql = '''SELECT `вещи`.`название`, `вещи`.`редкость`,
                    `магазин`.`количество`,`магазин`.`цена_покупки`, 
                    `магазин`.`цена продажи` 
                    FROM `магазин` 
                    INNER JOIN `вещи`
                    ON `вещи`.`id` = `магазин`.`id_вещи`'''
        self.cursor.execute(sql)
        ans = self.cursor.fetchone()
        self.shop_lst.clear()
        while (ans):
            txt = f'{ans[0]} {ans[1]} {ans[2]} {ans[3]} {ans[4]}'
            self.shop_lst.addItem(txt)
            ans = self.cursor.fetchone()
    
    def get_all_items(self):
        sql = 'SELECT * FROM `Вещи`'
        self.cursor.execute(sql)
        ans = self.cursor.fetchone()
        self.all_items_lst.clear()
        while (ans):
            txt = f'{ans[1]} {ans[2]} {ans[3]}'
            self.items_id_lst.append(ans[0])
            self.all_items_lst.addItem(txt)
            ans = self.cursor.fetchone()
            #id выбранной вещи лежит в отдельном списке

    def add_inventory(self):
        selected_number = self.all_items_lst.currentIndex()#это номер из списка id!!!
        selected_id = self.items_id_lst[selected_number]
        sql = 'INSERT INTO `Инвентарь`(`id_вещи`, `Количество`) VALUES(%s,1)'
        self.cursor.execute(sql, (selected_id,))
        self.connection.commit()
        self.show_inventory()


    def show_inventory(self):
        self.inventory_lst.clear()
        sql = '''SELECT `Вещи`.`название`, `Вещи`.`цена`, `Вещи`.`редкость`,
        `Инвентарь`.`количество`, `Инвентарь`.`id`
        FROM `Инвентарь`
        INNER JOIN `Вещи`
        ON `Инвентарь`.`Id_вещи` = `Вещи`.`id`;'''
        self.cursor.execute(sql)
        ans = self.cursor.fetchone()
        while ans:
            self.inventory_lst.addItem(f'{ans[0]} {ans[1]} {ans[2]} {ans[3]}')
            self.inventory_items_id.append(ans[4])
            ans = self.cursor.fetchone()

    def sel_item(self):
        if self.inventory_lst.currentIndex() is not None:
            print('можно продать')
            #найти как убрать выделение
            selected_item = self.inventory_lst.currentRow()
            print(selected_item)
            selected_id = self.inventory_items_id[selected_item]#id выбранной записи в инвентаре
            sql = "SELECT `id_вещи` FROM `Инвентарь`"
            self.cursor.execute(sql)
            ans = self.cursor.fetchone()#id выбранной вещи
            sql = 'DELETE FROM `Инвентарь` WHERE id=%s'
            self.cursor.execute(sql,(selected_id,))
            self.connection.commit()
            sql = "INSERT INTO `Магазин`(`id_вещи`,`количество`) VALUES(%s, 1)"
            self.cursor.execute(sql,(ans[0],))
            self.get_shop()
            self.show_inventory()



    def buy_item(self):
        if self.shop_lst.currentIndex() is not None:
            print("можно купить")
            #найти как убрать выделение


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyleSheet(Path('login.qss').read_text(encoding='utf-8'))
    window = MainWindow()
    sys.exit(app.exec())
