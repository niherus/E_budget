from PyQt5 import QtWidgets, QtSql
import sys

import os

class DatabaseError(Exception):
    def __init__(self, message):
        self.message = message



app = QtWidgets.QApplication(sys.argv)
con1 = QtSql.QSqlDatabase.addDatabase('QSQLITE')
filePath = './hope.db'
if  os.path.isfile(filePath):
    print('Ok')
    con1.setDatabaseName(filePath)
    con1.open()
else:
    raise DatabaseError("Database doesn't exist")
print(con1.size())