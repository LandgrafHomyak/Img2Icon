import sys

from PyQt5.QtCore import QCoreApplication
from PyQt5.QtWidgets import QApplication

from gui.window import Window
from resources import resources
from svg import Svg
from template import template


class TERMINAL:
    qapp = QCoreApplication

    @staticmethod
    def init(self):
        pass

    @staticmethod
    def run(self):
        pass

class GUI:
    qapp = QApplication

    @staticmethod
    def init(self):
        resources.open("intro.ico-button", "ico_button.svg", Svg)
        resources.open("intro.cur-button", "cur_button.svg", Svg)
        resources.open("intro.hover", "intro_hover.svg", Svg)
        resources.open("intro.clicked", "intro_clicked.svg", Svg)

        self.__window = Window()

    @staticmethod
    def run(self):
        self.__window.show()
        self.__window.setIntro()


@template.decorator("VARIANT")
class App:
    def __init__(self):
        self.__qapp = self.VARIANT.qapp(sys.argv)
        self.VARIANT.init(self)

    def run(self):
        self.VARIANT.run(self)
        self.__qapp.exec()
