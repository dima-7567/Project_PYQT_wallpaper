import sys
from PyQt5 import QtWidgets
from app import Loop


class App:
    def __init__(self):
        super().__init__()
        app = QtWidgets.QApplication(sys.argv)
        ex = Loop()
        ex.show()
        app.exec()


app = App()


