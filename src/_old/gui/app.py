from PyQt5.QtWidgets import QApplication

from _old.storage import Storage
from _old.gui.window import WindowMulti, WindowSingle


class GuiAppMulti:
    def __init__(self):
        self.qapp = QApplication([])
        self.window = WindowMulti()
        self.storage = Storage(self.window.files_list_widget(), self.window.to_empty, self.window.to_workspace)
        self.window.set_callbacks(self.storage.add, self.storage.get)

    def run(self):
        self.window.show()
        self.qapp.exec()

class GuiAppSingle:
    def __init__(self):
        self.qapp = QApplication([])
        self.window = WindowSingle()
        self.storage = None
        # self.window.set_callbacks(self.storage.add, self.storage.get)

    def run(self):
        self.window.show()
        self.qapp.exec()
