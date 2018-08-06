from PyQt5 import QtCore,QtWidgets,QtGui
from datetime import date
from database_logic import Db_control

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
        Menu_el_list = [["File","Open", "Save", "Save as", "Export", "Exit"],
                        ["Edit","Copy","Paste"],
                        ["Help", "Documentation", "Check an update", "About"]]
        print(len(Menu_el_list))
        for i in range(len(Menu_el_list)):
            print(Menu_el_list[i][0],end=': \n')
            exec('self.%s = QtWidgets.QMenu("%s")' % (("menu" +
                                                       Menu_el_list[i][0].replace(" ","_")),Menu_el_list[i][0].replace(" ","_")))
            for j in range(len(Menu_el_list[i])-1):
                print("  "+ Menu_el_list[i][j+1])
                exec('self.%s = QtWidgets.QAction("%s", None)' %
                     (("act" + Menu_el_list[i][j+1].replace(" ","_")),
                      Menu_el_list[i][j+1].replace(" ","_")))
                exec('self.%s.addAction(self.%s)' % (("menu" + Menu_el_list[i][0].replace(" ","_")),
                                                     ("act" + Menu_el_list[i][j+1].replace(" ","_"))))
            exec('self.menuBar().addMenu(self.%s)' %
                 ("menu" + Menu_el_list[i][0].replace(" ","_")))

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
        #######Подключаем базу данных
        self.fin_base = Db_control("finanse_base.db", default=True)
        self.layout = QtWidgets.QVBoxLayout(self)
        ########создаем вкладки
        self.tabs = QtWidgets.QTabWidget()
        self.tabs.resize(487, 280)
        #Вкладка расходы
        self.spents_tab = QtWidgets.QWidget()
        self.tabs.addTab(self.spents_tab, "Расходы")
        self.spents_tab.layout = QtWidgets.QVBoxLayout(self)
        self.spents_table = QtWidgets.QTableView()
        self.spents_model = QtGui.QStandardItemModel(1, 6)
        self.num = []
        column_names = ["Сумма", "Валюта", "Счет", "Дата", "Категория трат", "Примечание"]
        self.fin_base.create_table("Spent",column_names,['TEXT'] * len(column_names))
        self.fin_base.commite_changes()
        spent_data = self.fin_base.get_data("Spent")
        for raw in spent_data:
            L = []
            for i in range(1,len(raw)):
                L.append(QtGui.QStandardItem("{0}".format(raw[i], checkable=True)))
            self.spents_model.insertRow(0,L)
        self.spents_model.setHorizontalHeaderLabels(column_names)
        self.spents_table.setModel(self.spents_model)
        self.hHeader = self.spents_table.horizontalHeader()
        self.hHeader.setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
        self.btnAddRawSpent = QtWidgets.QPushButton('&Внести расходы')
        self.btnAddRawSpent.clicked.connect(self.click_event_spent)
        self.spents_tab.layout.addWidget(self.spents_table)
        self.spents_tab.layout.addWidget(self.btnAddRawSpent, alignment=QtCore.Qt.AlignLeft)
        self.spents_tab.setLayout(self.spents_tab.layout)
        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)

        #Вкладка доходы
        self.income_tab = QtWidgets.QWidget()
        self.tabs.addTab(self.income_tab, "Доходы")
        self.income_tab.layout = QtWidgets.QVBoxLayout(self)
        self.income_table = QtWidgets.QTableView()
        self.income_model = QtGui.QStandardItemModel(1, 6)
        self.num = []
        column_names = ["Сумма", "Валюта", "Счет", "Дата", "Источник", "Примечание"]
        self.fin_base.create_table("Income", column_names, ['TEXT'] * len(column_names))
        self.fin_base.commite_changes()
        income_data = self.fin_base.get_data("Income")
        for raw in income_data:
            L = []
            for i in range(1, len(raw)):
                L.append(QtGui.QStandardItem("{0}".format(raw[i], checkable=True)))
            self.income_model.insertRow(0, L)
        self.income_model.setHorizontalHeaderLabels(column_names)
        self.income_table.setModel(self.income_model)
        self.hHeader = self.income_table.horizontalHeader()
        self.hHeader.setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
        self.btnAddRawIncome = QtWidgets.QPushButton('&Внести доходы')
        self.btnAddRawIncome.clicked.connect(self.click_event_income)
        self.income_tab.layout.addWidget(self.income_table)
        self.income_tab.layout.addWidget(self.btnAddRawIncome, alignment=QtCore.Qt.AlignLeft)
        self.income_tab.setLayout(self.income_tab.layout)
        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)

        #Вкладка анализ (рекомедуемые ежедненые расходы на основные категории,
        #остаток до целей накопления, круговык диграммы расходов/доходов, динамика
        #расходов/доходов в заданный период)
        self.tab3 = QtWidgets.QWidget()
        self.tabs.addTab(self.tab3, "Анализ финансов")


    ######Эвенты кнопок
    def click_event_spent(self):
        dialog = Add_spent(self.spents_tab)
        dialog.accepted.connect(self.on_accepted)
        dialog.rejected.connect(self.on_rejected)
        dialog.finished[int].connect(self.on_finished)
        result = dialog.exec_()
        self.new_raw = []
        if result == QtWidgets.QDialog.Accepted:
            self.new_raw.append(dialog.money.text())
            self.new_raw.append(dialog.valuta.currentText())
            self.new_raw.append(dialog.op_type.currentText())
            self.new_raw.append(str(date.today()))
            self.new_raw.append(dialog.spent_type.currentText())
            self.new_raw.append(dialog.Big_text.toPlainText())
            self.fin_base.add_raw("Spent",self.new_raw)
            self.fin_base.commite_changes()
            L = []
            for i in range(0, len(self.new_raw)):
                L.append(QtGui.QStandardItem("{0}".format(self.new_raw[i],checkable = True)))
            self.spents_model.insertRow(0, L)
            self.spents_table.setModel(self.spents_model)
        else:
            print("Нажата кнопка Cancel, кнопка Закрыть или клавиша <Esc>",
                  result)

    def click_event_income(self):
        dialog = Add_income(self.income_tab)
        dialog.accepted.connect(self.on_accepted)
        dialog.rejected.connect(self.on_rejected)
        dialog.finished[int].connect(self.on_finished)
        result = dialog.exec_()
        self.new_raw = []
        if result == QtWidgets.QDialog.Accepted:
            self.new_raw.append(dialog.money.text())
            self.new_raw.append(dialog.valuta.currentText())
            self.new_raw.append(dialog.op_type.currentText())
            self.new_raw.append(str(date.today()))
            self.new_raw.append(dialog.income_type.currentText())
            self.new_raw.append(dialog.Big_text.toPlainText())
            self.fin_base.add_raw("Income", self.new_raw)
            self.fin_base.commite_changes()
            L = []
            for i in range(0, len(self.new_raw)):
                L.append(QtGui.QStandardItem("{0}".format(self.new_raw[i],checkable = True)))
            self.income_model.insertRow(0, L)
            self.income_table.setModel(self.income_model)
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
        self.setWindowTitle("Добавьте расходы")
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

class Add_income(QtWidgets.QDialog):
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
        self.income_type = QtWidgets.QComboBox(self)
        self.income_type.addItems(["Зарплата", "Продажа", "Возврат долгов", "Накопительный счет", "Вклады"])
        self.income_type.setFixedWidth(80)
        self.one_level.addWidget(self.money)
        self.one_level.addWidget(self.valuta)
        self.one_level.addWidget(self.op_type)
        self.one_level.addWidget(self.income_type)
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