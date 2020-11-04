from PyQt5.QtWidgets import QMainWindow

from gui.file_managment.input import InputArea
from gui.widgets import RootFrameWorkspace


class Window(QMainWindow):
    # add_to_storage_signal = pyqtSignal(object)
    def __init__(self):
        super().__init__()
        self.__root_empty = InputArea(self, self.__request_uploading)
        self.__root_list = RootFrameWorkspace(self, self.__request_uploading, self.__get_slot)
        self.__root_list.hide()
        self.setCentralWidget(self.__root_empty)
        self.__request_uploading = None

    def files_list_widget(self):
        return self.__root_list.files_list_widget()

    def set_callbacks(self, request_uploading, get_slot):
        self.__request_uploading = request_uploading
        self.__get_slot = get_slot

    def __on_first_file_added(self, location):
        self.__to_workspace()
        self.__request_uploading(location)

    def __request_uploading(self, location):
        self.__request_uploading(location)

    def __get_slot(self, y):
        self.__get_slot(y)

    def to_workspace(self):
        if self.centralWidget() is not self.__root_list:
            self.__root_empty.hide()
            self.setCentralWidget(self.__root_list)
            self.__root_list.show()

    def to_empty(self):
        if self.centralWidget() is not self.__root_empty:
            self.__root_list.show()
            self.setCentralWidget(self.__root_empty)
            self.__root_empty.hide()
