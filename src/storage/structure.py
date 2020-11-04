from PyQt5.QtCore import QObject, pyqtSignal

from storage.loader import Loader
from storage.table_controller import TableController


class Storage(QObject):
    __slots__ = ("__list", "__loader", "__controller")

    __set_empty_signal = pyqtSignal()
    __set_workspace_signal = pyqtSignal()

    def __init__(self, files_list_widget, set_empty_callback, set_workspace_callback):
        super().__init__()
        self.__set_empty_signal.connect(set_empty_callback)
        self.__set_workspace_signal.connect(set_workspace_callback)
        self.__list = ListWithCallbacks(self.__set_empty_signal.emit, self.__set_workspace_signal.emit)
        self.__loader = Loader()
        self.__controller = TableController(files_list_widget, self.__loader.add, self.__store_slot)

    def add(self, input):
        self.__controller.add(input)

    def __store_slot(self, slot):
        self.__list.append(slot)

    def get(self, y):
        return self.__list[y]


class ListWithCallbacks(list):
    __slots__ = ("__set_empty_callback", "__set_workspace_callback")

    def __init__(self, set_empty_callback, set_workspace_callback):
        super().__init__()
        self.__set_empty_callback = set_empty_callback
        self.__set_workspace_callback = set_workspace_callback

    def append(self, __object):
        if len(self) == 0:
            self.__set_workspace_callback()
        super().append(__object)

    def pop(self, __index):
        if len(self) == 1:
            self.__set_empty_callback()
        return super().pop(__index)
