from collections import deque
from functools import lru_cache
from typing import NoReturn, Union, List

from PyQt5.QtCore import QUrl, QThread, QRect, QSize, QRectF
from PyQt5.QtGui import QImage, QPainter, QPixmap, QIcon
from PyQt5.QtSvg import QSvgRenderer
from PyQt5.QtXml import QDomDocument

from storage.slot import Slot


class Loader(QThread):
    __queue: deque[Slot] = ...

    def __init__(self) -> NoReturn: ...

    def add(self, slot) -> NoReturn: ...

    def run(self) -> NoReturn: ...


class LoadRequest:
    pass


class FileOnPath(LoadRequest):
    s: str = ...

    def __init__(self, path: str): ...


class FileOnURL(LoadRequest):
    s: str = ...

    def __new__(cls, url: Union[QUrl, str]) -> Union[FileOnPath, FileOnURL]: ...

    def __init__(self, url: Union[QUrl, str]) -> NoReturn: ...


class Error(LoadRequest):
    pass
