from functools import lru_cache

from PyQt5.QtCore import QObject, pyqtSignal, QRect, QSize, QRectF
from PyQt5.QtGui import QImage, QIcon, QPainter, QPixmap
from PyQt5.QtSvg import QSvgRenderer
from PyQt5.QtXml import QDomDocument


class Slot(QObject):
    __slots__ = ("prepared", "original", "location", "row")

    in_order_signal = pyqtSignal()
    processing_signal = pyqtSignal()
    complete_signal = pyqtSignal()
    error_signal = pyqtSignal()
    update_preview_signal = pyqtSignal(object)

    def __init__(self, location, row):
        super().__init__()
        self.location = location
        self.original = None
        self.prepared = None

        # def set_row(self, row):
        self.row = row
        self.in_order_signal.connect(row.state.in_order)
        self.processing_signal.connect(row.state.processing)
        self.complete_signal.connect(row.state.complete)
        self.error_signal.connect(row.state.error)
        self.update_preview_signal.connect(row.preview.set_prepared_image)

    def in_order(self):
        self.in_order_signal.emit()

    def processing(self):
        self.processing_signal.emit()

    def complete(self):
        self.complete_signal.emit()

    def error(self):
        self.error_signal.emit()

    def update(self):
        self.update_preview_signal.emit(self.prepared)


class PreparedImage:
    def to_bitmap(self, size):
        raise NotImplementedError

    def free_resize(self):
        raise NotImplementedError

    def available_sizes(self):
        raise NotImplementedError

    def render(self, painter, rect):
        raise NotImplementedError

    def size(self):
        raise NotImplementedError

    def prerendered(self):
        raise NotImplementedError


class PreparedBitmap(PreparedImage):
    __slots__ = ("img",)

    def __init__(self, qimage):
        self.img = qimage

    def to_bitmap(self, size):
        QIcon(self.img).pixmap(size)

    def free_resize(self):
        return False

    def available_sizes(self):
        return QIcon(self.img).availableSizes()

    def render(self, painter, rect):
        painter.drawImage(rect, self.img)

    def size(self):
        return self.img.size()

    def prerendered(self):
        return self.img


class PreparedSVG(PreparedImage):
    __slots__ = ("dom", "__prerendered")

    def __init__(self, qdom):
        self.dom = qdom
        # self.__prerendered = QImage(self.size(), QImage.Format_ARGB32)
        # painter = QPainter(self.__prerendered)
        # self.render(painter, QRect(0, 0, self.size().width(), self.size().height()))

    def to_bitmap(self, size):
        pixmap = QPixmap()
        painter = QPainter(pixmap)
        self.render(painter, QRect(0, 0, size.width() - 1, size.height() - 1))
        return pixmap

    def free_resize(self):
        return True

    def render(self, painter, rect):
        QSvgRenderer(self.dom.toByteArray()).render(painter, QRectF(rect))

    def size(self):
        return QSize(float(self.dom.documentElement().attribute("width")),
                     float(self.dom.documentElement().attribute("height")))

    def prerendered(self):
        return self.__prerendered
