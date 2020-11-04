from PyQt5.QtWidgets import QApplication

from storage import Storage
from gui.window import Window


class GuiApp:
    def __init__(self):
        self.qapp = QApplication([])
        self.window = Window()
        self.storage = Storage(self.window.files_list_widget(), self.window.to_empty, self.window.to_workspace)
        self.window.set_callbacks(self.storage.add, self.storage.get)

    def run(self):
        self.window.show()
        self.qapp.exec()
