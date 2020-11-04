from PyQt5.QtWidgets import QFrame, QGridLayout

from gui.file_managment.files_list import FilesList, HasFilesListWidget
from gui.file_managment.input import InputArea


class FileManager(QFrame, HasFilesListWidget):
    __slots__ = ("__layout", "__input_area", "__files_list")

    def __init__(self, parent, request_uploading, set_selected_slot_number):
        super().__init__(parent)
        self.__layout = QGridLayout(self)
        self.setLayout(self.__layout)

        self.__files_list = FilesList(self, set_selected_slot_number)
        self.__layout.addWidget(self.__files_list, 0, 0, 1, 1)

        self.__input_area = InputArea(self, request_uploading)
        self.__layout.addWidget(self.__input_area, 1, 0, 1, 1)

    def files_list_widget(self):
        return self.__files_list
