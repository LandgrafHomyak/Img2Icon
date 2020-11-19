from PyQt5.QtWidgets import QMainWindow

from _old.gui.file_managment import InputArea
from _old.gui.widgets import RootFrameWorkspace
from _old.gui.workspace.frame import Workspace


class WindowMulti(QMainWindow):
    # add_to_storage_signal = pyqtSignal(object)
    def __init__(self):
        super().__init__()
        self.__root_empty = InputArea.Multi(self, self.__request_uploading)
        self.__root_list = RootFrameWorkspace(self, self.__request_uploading, self.__get_slot)
        self.__root_list.hide()
        self.setCentralWidget(self.__root_empty)
        self.__request_uploading_v = None
        self.__get_slot_v = None

    def files_list_widget(self):
        return self.__root_list.files_list_widget()

    def set_callbacks(self, request_uploading, get_slot):
        self.__request_uploading_v = request_uploading
        self.__get_slot_v = get_slot

    def __on_first_file_added(self, location):
        self.__to_workspace()
        self.__request_uploading_v(location)


    def __get_slot(self, y):
        return self.__get_slot_v(y)

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


class WindowSingle(QMainWindow):
    def __init__(self):
        super().__init__()
        self.__root_select = InputArea.Single(self, self.__request_uploading)
        self.__root_workspace = Workspace(self)
        self.__root_workspace.hide()
        self.setCentralWidget(self.__root_empty)
        self.__request_uploading_v = None
        self.__get_slot_v = None

    def __request_uploading(self, location):
        self.__request_uploading_v(location)