from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QFrame, QGridLayout, QFileDialog, QTableWidget

from gui.file_managment import FileManager, HasFilesListWidget
from gui.workspace.frame import Workspace


class RootFrameWorkspace(QFrame, HasFilesListWidget):
    __set_slot = pyqtSignal(object)
    def __init__(self, parent, request_uploading, get_slot_by_number):
        super().__init__(parent)

        self.add_to_storage = request_uploading

        self.__layout = QGridLayout(self)
        self.setLayout(self.__layout)

        self.__file_manager = FileManager(self, request_uploading, self.__set_selected_slot_number)
        self.__layout.addWidget(self.__file_manager, 0, 0, 1, 1)

        self.__workspace = Workspace(self)
        self.__layout.addWidget(self.__workspace, 0, 1, 1, 1)

        self.__set_slot.connect(self.__workspace.set_slot)
        self.__get_slot_by_number = get_slot_by_number

    def files_list_widget(self):
        return self.__file_manager.files_list_widget()

    def __set_selected_slot_number(self, y):
        self.__set_slot.emit(self.__get_slot_by_number(y))

