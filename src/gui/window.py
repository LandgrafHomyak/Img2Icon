from PyQt5.QtWidgets import QMainWindow

from gui.intro import Intro


class Window(QMainWindow):
    def __init__(self):
        super().__init__()

        self.__intro_frame = Intro(self, self.setICO, self.setCUR)
        self.__ico_frame = None
        self.__cur_frame = None

    def setIntro(self):
        self.setCentralWidget(self.__intro_frame)

    def setICO(self):
        self.setCentralWidget(self.__ico_frame)

    def setCUR(self):
        self.setCentralWidget(self.__cur_frame)
