from PyQt5 import QtWidgets
from win_logic import MyWindow
import sys


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    ex = MyWindow()
    sys.exit(app.exec_())

