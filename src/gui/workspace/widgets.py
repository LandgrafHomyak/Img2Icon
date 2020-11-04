from PyQt5.QtCore import QSize
from PyQt5.QtGui import QImage, QPaintEvent
from PyQt5.QtWidgets import QWidget, QFrame, QTableWidget


class ImagePreview(QWidget):
    __slots__ = ("image_to_render", "prerendered_image", "prerendered_size")

    def __init__(self, parent):
        super().__init__(parent=parent)
        self.image_to_render = None
        self.prerendered_size = QSize(-1, -1)
        self.prerendered_image = QImage()

    def paintEvent(self, event: QPaintEvent) -> None:
        return
        if self.image_to_render is not None:
            painter = QPainter(self)
            window = self.size()
            image = self.image_to_render.size()
            if image.width() <= 0 or image.height() <= 0:
                return
            if window.height() / image.height() < window.width() / image.width():
                render = QSize(window.height() * image.width() // image.height(), window.height())
            else:
                render = QSize(window.width(), window.width() * image.height() // image.width())

            # if render != self.prerendered_size:
            #     self.prerendered_size = render
            #     self.prerendered_image = QImage(render, QImage.Format_ARGB32)
            #     ipainter = QPainter(self.prerendered_image)
            #     self.image_to_render.render(ipainter, QRectF(0, 0, render.width(),
            #                                                  render.height()))
            painter.drawImage(
                QRect((window.width() - render.width()) // 2, (window.height() - render.height()) // 2,
                      render.width(), render.height()), self.image_to_render.prerendered())

    def set_prepared_image(self, prepared_image):
        self.image_to_render = prepared_image
        self.update()


class Output(QFrame):
    def __init__(self, parent):
        super().__init__(parent=parent)


class Resize(QFrame):
    def __init__(self, parent):
        super().__init__(parent=parent)


class AvailableSizes(QTableWidget):
    def __init__(self, parent):
        super().__init__(parent=parent)
