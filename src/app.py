import sys

from PyQt5.QtCore import QCoreApplication
from PyQt5.QtWidgets import QApplication

from template import template


class TERMINAL:
    qapp = QCoreApplication


class GUI:
    qapp = QApplication


@template.decorator("VARIANT")
class App:
    def __init__(self):
        self.qapp = self.VARIANT.qapp(sys.argv)

    def run(self):
        self.qapp.exec()
