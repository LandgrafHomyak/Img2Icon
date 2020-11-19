from collections import deque
from os.path import splitext

from PyQt5.QtCore import QUrl, QThread, QFile, QIODevice
from PyQt5.QtGui import QImage
from PyQt5.QtXml import QDomDocument

from _old.storage import Slot, PreparedBitmap, PreparedSVG


class Loader(QThread):
    __slots__ = ("__queue",)

    def __init__(self):
        super().__init__()
        self.__queue = deque()

    def add(self, slot):
        if not isinstance(slot, Slot):
            raise TypeError("Slot")
        self.__queue.append(slot)
        if not self.isRunning():
            self.start()

    def run(self):
        while self.__queue:
            slot = self.__queue.popleft()
            if isinstance(slot.location, FileOnPath):
                slot.processing()
                if slot.location.s:
                    if splitext(slot.location.s)[1] == ".svg":
                        file = QFile(slot.location.s)
                        if file.open(QIODevice.ReadOnly | QIODevice.Text):
                            slot.original = QDomDocument()
                            slot.original.setContent(file)
                            slot.prepared = PreparedSVG(slot.original)
                            slot.complete()
                            slot.update()
                        else:
                            slot.error()
                    else:
                        slot.original = QImage(slot.location.s)
                        slot.prepared = PreparedBitmap(slot.original)
                        slot.complete()
                        slot.update()
                else:
                    slot.error()
            else:
                slot.error()



class LoadRequest:
    pass


class FileOnPath(LoadRequest):
    __slots__ = ("s",)

    def __init__(self, path):
        if isinstance(path, str):
            self.s = str(path)
        else:
            raise TypeError("path must be a 'str'")


class FileOnURL(LoadRequest):
    __slots__ = ("s",)

    def __new__(cls, url):
        if isinstance(url, QUrl):
            if url.isLocalFile():
                return FileOnPath(url.toLocalFile())
            else:
                return super().__new__(cls)
        return super().__new__(cls)

    def __init__(self, url):
        if isinstance(url, QUrl):
            self.s = str(url.toString())
        elif isinstance(url, str):
            self.s = str(url)
        else:
            raise TypeError("URL must be a 'str' or 'PyQt5.QtCore.QUrl'")


class Error(LoadRequest):
    pass
