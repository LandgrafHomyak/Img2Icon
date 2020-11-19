from PyQt5.QtCore import QEvent, QRectF
from PyQt5.QtGui import QMouseEvent, QPaintEvent, QPainter, QColor, QPen, QResizeEvent
from PyQt5.QtWidgets import QFrame, QWidget, QHBoxLayout, QSizePolicy

from resources import resources


class Intro(QFrame):
    __slots__ = ("__ico_button", "__cur_button", "__layout")

    def __init__(self, parent, ico_callback, cur_callback):
        super().__init__(parent)

        self.__layout = QHBoxLayout(self)

        self.__ico_button = Button(self, resources["intro.ico-button"], ico_callback)
        self.__splitter = Splitter(self)
        self.__cur_button = Button(self, resources["intro.cur-button"], cur_callback)

    def resizeEvent(self, event: QResizeEvent) -> None:
        w = self.width() - 1

        self.__ico_button.move(0, 0)
        self.__ico_button.resize(w // 2, self.height())

        self.__splitter.move(w // 2, (self.height() - min(self.height(), w // 2)) // 2)
        self.__splitter.resize(1, min(self.height(), w // 2))

        self.__cur_button.move(self.width() - w // 2, 0)
        self.__cur_button.resize(w // 2 + 1, self.height())


class Button(QWidget):
    __slots__ = ("__svg", "__state", "__callback")

    def __init__(self, parent, svg, callback):
        super().__init__(parent)
        self.__state = ButtonState()
        self.__svg = svg
        self.__callback = callback

    def enterEvent(self, event: QEvent):
        self.__state.hover = True
        self.update()

    def leaveEvent(self, event: QEvent):
        self.__state.hover = False
        self.update()

    def mousePressEvent(self, event: QMouseEvent) -> None:
        self.__state.clicked = True
        self.update()

    def mouseReleaseEvent(self, event: QMouseEvent) -> None:
        self.__state.clicked = False
        self.update()
        if self.__state.hover:
            self.__callback()

    def paintEvent(self, event: QPaintEvent) -> None:
        painter = QPainter(self)

        size = min(self.width(), self.height())
        rect = QRectF((self.width() - size) // 2, (self.height() - size) // 2, size, size)
        if self.__state.clicked:
            resources["intro.clicked"].renderer.render(painter, rect)
        elif self.__state.hover:
            resources["intro.hover"].renderer.render(painter, rect)

        self.__svg.renderer.render(painter, rect)


class Splitter(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.setFixedWidth(1)
        self.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.MinimumExpanding)

    def paintEvent(self, event: QPaintEvent) -> None:
        painter = QPainter(self)
        painter.setPen(QPen(QColor(0x000000)))
        painter.drawLine(0, 0, 0, self.height())


class ButtonState:
    __slots__ = ("hover", "clicked")

    def __init__(self):
        self.hover = False
        self.clicked = False
