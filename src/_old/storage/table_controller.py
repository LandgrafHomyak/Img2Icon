from collections import deque

from PyQt5.QtCore import QThread, pyqtSignal

from _old.storage import FileOnPath, FileOnURL, Error
from _old.storage import Slot


class TableController(QThread):
    __slots__ = ("__queue", "__widget", "__store_slot", "__load_slot", "__thread_blocked")

    __add_rows_signal = pyqtSignal(int, object)

    def __init__(self, widget, load_slot, store_slot):
        super().__init__()
        self.__queue = deque()
        self.__widget = widget
        self.__add_rows_signal.connect(self.__widget.add_rows)
        self.__load_slot = load_slot
        self.__store_slot = store_slot
        self.__thread_blocked = False

    def add(self, input):
        if not isinstance(input, InputEntity):
            raise TypeError("InputEntity")
        self.__queue.append(input)
        if not self.isRunning():
            self.start()

    def run(self):
        while self.__queue:
            request = self.__queue.popleft()
            if isinstance(request, FileDialogInput):
                slen = len(self.__widget)
                count = len(request)
                self.__add_rows(count)
                for y in range(count):
                    slot = Slot(FileOnPath(request[y]), self.__widget.get_row(y + slen))
                    slot.in_order()
                    self.__store_slot(slot)
                    self.__load_slot(slot)
            elif isinstance(request, DragAndDropInput):
                if request.is_url():
                    slen = len(self.__widget)
                    count = len(request)
                    self.__add_rows(count)
                    for y in range(count):
                        slot = Slot(
                            FileOnPath(request[y].toLocalFile()) if request[y].isLocalFile() else FileOnURL(request[y]),
                            self.__widget.get_row(y + slen))
                        slot.in_order()
                        self.__store_slot(slot)
                        self.__load_slot(slot)
                else:
                    self.__add_rows(1)
                    self.__error_slot()
            else:
                self.__add_rows(1)
                self.__error_slot()

    def __add_rows(self, count):
        self.__add_rows_signal.emit(count, self.__unblock_thread)
        self.__thread_blocked = True
        while self.__thread_blocked:
            pass

    def __unblock_thread(self):
        self.__thread_blocked = False

    def __error_slot(self):
        self.__add_rows(1)
        slot = Slot(Error, self.__widget.get_row(len(self.__widget) - 1))
        slot.error()
        self.__store_slot(slot)


class InputEntity:
    pass


def FileDialogInput(entity):
    paths = entity[0]
    if isinstance(paths, str):
        return FileDialogSingleInput(paths)
    elif isinstance(paths, list):
        return FileDialogMultiInput(paths)


class FileDialogMultiInput(InputEntity):
    __slots__ = ("__list",)

    def __init__(self, entity):
        self.__list = entity

    def __len__(self):
        return len(self.__list)

    def __getitem__(self, i):
        return self.__list[i]

    def __iter__(self):
        return iter(self.__list)


class FileDialogSingleInput(InputEntity):
    __slots__ = ("__str",)

    def __init__(self, entity):
        self.__str = entity

    def __str__(self):
        return self.__str


class DragAndDropInput(InputEntity):
    __slots__ = ("__entity",)

    def __init__(self, entity):
        self.__entity = entity

    def is_image(self):
        return self.__entity.hasImage()

    def is_url(self):
        return self.__entity.hasUrls()

    def __getitem__(self, i):
        return self.__entity.urls()[i]

    def __iter__(self):
        return iter(self.__entity.urls())

    def __len__(self):
        return len(self.__entity.urls())
