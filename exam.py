"""
экзамен 13.01
подгруппа1 9-00:
Погосян
Пеливан
Омуракунов
Попов
Ершов
Щипакин
Федорова
Крыканова
Якимова
Любарцов
Дич
Климанова
Львов
Кулаков
Яковлев
подгуппа2 11-00:
Иванов
Клыков
Кондратов
Левченко
Панцырев
Спиридович
Худойназаров
Читалкин


экзамен с интернетом, но вопросами
пользователя создать!!!
БД pymysql:
1. подключение
2. SELECT, INSERT, DELETE
3. INNER JOIN
Python
1. классы, параметры(поля), методы
2. циклы, списки
PyQt6
1. окно на базе Qwidget
2. раскладка QGridLayout
3. QLabel, QLineEdit, QComboBox, QListWidget, QPushButton
4. слоты и сигналы: clicked, activated, itemClicked, itemDoubleClicked
структура разработки
1. БД и таблицы
2. пользователь для БД
3. создать интерфейс
4. сделать подключение к БД
5. сделать логику ПО

"""
from PyQt6.QtWidgets import QApplication, QWidget, QLabel,\
    QLineEdit, QPushButton, QComboBox, QListWidget, QGridLayout
import sys
import pymysql.cursors
from typing import Any

class ExamApp(QWidget):
    def __init__(self):
        super().__init__()
        layout = QGridLayout()
        self.setLayout(layout)
        # создание элементов
        self.name_lbl = QLabel("Фамилия")
        self.group_lbl = QLabel("Группа")
        self.name_ent = QLineEdit()
        self.group_ent = QComboBox()
        self.main_lst = QListWidget()
        self.add_btn = QPushButton("Добавить")
        self.del_btn = QPushButton("Удалить")
        # размещение элементов
        layout.addWidget(self.main_lst,0,0,2,1)
        layout.addWidget(self.name_lbl,0,1)
        layout.addWidget(self.name_ent,0,2)
        layout.addWidget(self.group_lbl,1,1)
        layout.addWidget(self.group_ent,1,2)
        layout.addWidget(self.add_btn,2,0)
        layout.addWidget(self.del_btn,2,1,1,2)
        # сигналы
        self.add_btn.clicked.connect(self.add_student)
        self.del_btn.clicked.connect(self.del_student)
        self.db_handler()
        self.get_all_students()
        self.get_groups()
        self.show()

    # слоты
    def add_student(self):
        pass

    def del_student(self):
        pass

    # подключение к БД
    def db_handler(self):
        self.connection = pymysql.connect(
            host="localhost",
            user="exam_student",
            password="1234",
            database="pk31_exam"
        )
        self.cur = self.connection.cursor()

    #получение списка студентов
    def get_all_students(self):
        sql = """SELECT students.name, student_groups.name,
        student_groups.starosta 
        FROM students
        INNER JOIN student_groups
        ON students.st_group=student_groups.id
        """
        self.cur.execute(sql)
        ans: tuple[Any, ...] | None = self.cur.fetchone()
        self.main_lst.clear()
        while ans:
            txt: str = f"{ans[0]} {ans[1]} {ans[2]}"
            self.main_lst.addItem(txt)
            ans = self.cur.fetchone()

    # получение групп и запись в QComboBox
    def get_groups(self):
        sql = "SELECT * FROM student_groups"
        self.cur.execute(sql)
        ans: tuple[Any, ...] | None = self.cur.fetchone()
        self.group_ent.clear()
        while ans:
            txt = f"{ans[1]}"
            self.group_ent.addItem(txt)
            ans = self.cur.fetchone()

app = QApplication(sys.argv)
my_app = ExamApp()
sys.exit(app.exec())


