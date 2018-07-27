from PyQt5 import QtCore,QtWidgets,QtGui
from datetime import date
import time
import sys


class MyWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("E-budget")
        desktop = QtWidgets.QApplication.desktop()
        self.WinWidth = 487
        self.WinHeigth = 280
        self.move(desktop.width() - self.WinWidth - 10
                  , desktop.height() - self.WinHeigth - 20)
        self.setFixedSize(self.WinWidth,self.WinHeigth)

        ######Создаем вкладки
        self.tablet_widget = MyWidget(self)
        self.setCentralWidget(self.tablet_widget)
        self.add_menu()
        self.show()

    def add_menu(self):
        ######Составляем меню
        Menu_el_list = [["File","Open", "Save", "Save as", "Export", "Exit"],["Edit","Copy","Paste"],["Help", "Documentation", "Check an update", "About"]]
        print(len(Menu_el_list))
        for i in range(len(Menu_el_list)):
            print(Menu_el_list[i][0],end=': \n')
            exec('self.%s = QtWidgets.QMenu("%s")' % (("menu" + Menu_el_list[i][0].replace(" ","_")),Menu_el_list[i][0].replace(" ","_")))
            for j in range(len(Menu_el_list[i])-1):
                print("  "+ Menu_el_list[i][j+1])
                exec('self.%s = QtWidgets.QAction("%s", None)' % (("act" + Menu_el_list[i][j+1].replace(" ","_")),Menu_el_list[i][j+1].replace(" ","_")))
                exec('self.%s.addAction(self.%s)' % (("menu" + Menu_el_list[i][0].replace(" ","_")),("act" + Menu_el_list[i][j+1].replace(" ","_"))))
            exec('self.menuBar().addMenu(self.%s)' % ("menu" + Menu_el_list[i][0].replace(" ","_")))

    def on_open(self):
        print("Выбран пункт меню Open")

    def on_help(self):
        print("Выбран пункт меню Help")

    def on_hovered(self, act):
        print("on_hovered", act.text())

    def on_triggered(self, act):
        print("on_triggered", act.text())


#######Начинка основного окна
class MyWidget(QtWidgets.QWidget):
    ######Расстановка элементов при запуске
    def __init__(self, parent):
        super(QtWidgets.QWidget, self).__init__(parent) ######Создаем главное окно
        self.layout = QtWidgets.QVBoxLayout(self)
        ########создаем вкладки
        self.tabs = QtWidgets.QTabWidget()
        self.tab1 = QtWidgets.QWidget()
        self.tab2 = QtWidgets.QWidget()
        self.tab3 = QtWidgets.QWidget()
        self.tabs.resize(487,280)
        self.tabs.addTab(self.tab1,"Расходы")
        self.tabs.addTab(self.tab2,"Доходы")
        self.tabs.addTab(self.tab3,"Анализ финансов")

        self.tab1.layout = QtWidgets.QVBoxLayout(self)
        self.table = QtWidgets.QTableView()
        self.model = QtGui.QStandardItemModel(1, 6)
        self.num = []
        for row in range(0, 24):
           self.num.append(str(24-row))
           for column in range(0, 6):
            self.item = QtGui.QStandardItem("({0}, {1})".format(row, column))
            self.item.setEditable(False)
            self.item.setCheckable(True)
            self.model.setItem(row, column, self.item)
        self.model.setHorizontalHeaderLabels(["Сумма","Валюта","Тип операции","Дата","Категория трат","Примечание"])
        self.model.setVerticalHeaderLabels(self.num)
        self.table.setModel(self.model)
        self.hHeader = self.table.horizontalHeader()
        self.hHeader.setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
        self.btnAddRaw = QtWidgets.QPushButton('&Добавить расходы')
        self.btnAddRaw.clicked.connect(self.click_event)
        self.tab1.layout.addWidget(self.table)
        self.tab1.layout.addWidget(self.btnAddRaw, alignment=QtCore.Qt.AlignLeft)
        self.tab1.setLayout(self.tab1.layout)
        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)




    ######Эвенты кнопок
    def click_event(self):
        dialog = Add_spent(self.tab1)
        dialog.accepted.connect(self.on_accepted)
        dialog.rejected.connect(self.on_rejected)
        dialog.finished[int].connect(self.on_finished)
        result = dialog.exec_()
        self.new_raw = []
        if result == QtWidgets.QDialog.Accepted:
            self.new_raw.append(dialog.money.text())
            self.new_raw.append(dialog.valuta.currentText())
            self.new_raw.append(dialog.op_type.currentText())
            self.new_raw.append(str(date.today()) + " " + time.strftime("%H:%M"))
            self.new_raw.append(dialog.spent_type.currentText())
            self.new_raw.append(dialog.Big_text.toPlainText())
            L = []
            for i in range(0, 6):
                L.append(QtGui.QStandardItem("{0}".format(self.new_raw[i],checkable = True)))
            self.model.insertRow(0, L)
            self.table.setModel(self.model)
        else:
            print("Нажата кнопка Cancel, кнопка Закрыть или клавиша <Esc>",
                  result)
    def on_accepted(self):
        print("on_accepted")

    def on_rejected(self):
        print("on_rejected")

    def on_finished(self,text):
        print("Finised")



class Add_spent(QtWidgets.QDialog):
    def __init__(self, parent=None):
        QtWidgets.QDialog.__init__(self, parent)
        self.setWindowTitle("Диалоговое окно")
        self.resize(200, 70)
        self.mainBox = QtWidgets.QVBoxLayout()
        self.one_level = QtWidgets.QHBoxLayout()
        self.money = QtWidgets.QDoubleSpinBox()
        self.money.setButtonSymbols(2)
        self.money.setMaximum(10**10)
        self.money.setDecimals(2)
        self.money.setFixedWidth(50)
        self.valuta = QtWidgets.QComboBox(self)
        self.valuta.addItems(["Рубль","Доллар","Евро"])
        self.valuta.setFixedWidth(65)
        self.op_type = QtWidgets.QComboBox(self)
        self.op_type.setFixedWidth(80)
        self.op_type.addItems(["Наличные", "Карта"])
        self.spent_type = QtWidgets.QComboBox(self)
        self.spent_type.addItems(["Транспорт", "Еда", "Одежда", "Прочее"])
        self.spent_type.setFixedWidth(80)
        self.one_level.addWidget(self.money)
        self.one_level.addWidget(self.valuta)
        self.one_level.addWidget(self.op_type)
        self.one_level.addWidget(self.spent_type)

        self.label = QtWidgets.QLabel(self)
        self.label.setText("Примечание:")
        self.Big_text = QtWidgets.QTextEdit()
        self.four_level = QtWidgets.QHBoxLayout()
        self.btnOK = QtWidgets.QPushButton("&OK")
        self.btnCancel = QtWidgets.QPushButton("&Cancel")
        self.btnCancel.setDefault(True)
        self.btnOK.clicked.connect(self.accept)
        self.btnCancel.clicked.connect(self.reject)
        self.four_level.addWidget(self.btnOK)
        self.four_level.addWidget(self.btnCancel)
        self.two_level = QtWidgets.QHBoxLayout()
        self.two_level.addWidget(self.label)
        self.three_level = QtWidgets.QHBoxLayout()
        self.three_level.addWidget(self.Big_text)
        self.mainBox.addLayout(self.one_level)
        self.mainBox.addLayout(self.two_level)
        self.mainBox.addLayout(self.three_level)
        self.mainBox.addLayout(self.four_level)

        self.setLayout(self.mainBox)