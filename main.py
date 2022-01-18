from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QDialog
import os
import sys

from gui import Win

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setApplicationName('Курсовая работа')
    win = Win()
    app.exec_()