from enum import IntEnum, auto

from PyQt5.QtCore import QPoint, Qt, QMimeData
from PyQt5.QtGui import QDragEnterEvent, QDropEvent, QDragLeaveEvent, QPaintEvent, QPainter, QFont, \
    QFontMetrics, QPen, QColor, QBrush, QMouseEvent
from PyQt5.QtWidgets import QWidget, QPushButton, QGridLayout, QFrame, QFileDialog

from storage import FileDialogInput, DragAndDropInput


class InputArea(QFrame):
    __slots__ = ("__request_uploading", "__layout", "__drop_area", "__dialog_button")

    def __init__(self, parent, request_uploading):
        super().__init__(parent=parent)

        self.__request_uploading = request_uploading

        self.__layout = QGridLayout(self)
        self.setLayout(self.__layout)

        self.__drop_area = DropImage(self, request_uploading)
        self.__layout.addWidget(self.__drop_area, 0, 0)

        self.__dialog_button = QPushButton("Select file", self)
        self.__dialog_button.clicked.connect(self.file_dialog)
        self.__layout.addWidget(self.__dialog_button, 1, 0)

    def file_dialog(self):
        self.__request_uploading(FileDialogInput(QFileDialog.getOpenFileNames(self)[0]))


class DropImage(QWidget):
    class States(IntEnum):
        normal = auto()
        expected_type = auto()
        wrong_type = auto()

    __slots__ = ("__state", "__request_uploading")

    possible_mime_types = (
        "image/jpeg",
        "image/pjpeg",
        "image/png",
        "image/svg+xml",
        "image/tiff",
        "image/vnd.microsoft.icon"
    )

    # on_drop = pyqtSignal(object)

    def __init__(self, parent, request_uploading):
        super().__init__(parent)
        self.setAcceptDrops(True)
        self.__request_uploading = request_uploading
        self.__state = self.States.normal

    def dragEnterEvent(self, event: QDragEnterEvent):
        if event.mimeData().hasUrls() or event.mimeData().hasImage():
            event.acceptProposedAction()
            self.__state = self.States.expected_type
            self.update()
        else:
            event.acceptProposedAction()
            self.__state = self.States.wrong_type
            self.update()

    def dragLeaveEvent(self, event: QDragLeaveEvent):
        self.__state = self.States.normal
        self.update()

    def dropEvent(self, event: QDropEvent) -> None:
        self.__state = self.States.normal
        self.update()

        event.acceptProposedAction()
        source = event.mimeData()
        stable = QMimeData()
        if source.hasUrls():
            stable.setUrls(source.urls())
        self.__request_uploading(DragAndDropInput(stable))

    def paintEvent(self, event: QPaintEvent):
        painter = QPainter(self)

        font = QFont()
        font.setPixelSize(self.height() // 5)

        fm = QFontMetrics(font)
        # w = max(fm.width("Drop image here"), fm.width("Wrong image type"))
        # if w >= self.width():
        #     font.setPixelSize(fm.height() * (self.width() - 60) / w)

        painter.setFont(font)
        if self.__state == self.States.normal:
            painter.setPen(QPen(QColor(0xdddddd)))
            painter.setBrush(QBrush(QColor(0xdddddd)))
            painter.drawRect(0, 0, self.width(), self.height())
            painter.setPen(QPen(QColor(0x333333)))
            painter.setBrush(Qt.NoBrush)
            painter.drawText(QPoint((self.width() - fm.width("Drop image here")) // 2, self.height() * 3 // 5),
                             "Drop image here")
        elif self.__state == self.States.expected_type:
            painter.setPen(QPen(QColor(0xaaddaa)))
            painter.setBrush(QBrush(QColor(0xaaddaa)))
            painter.drawRect(0, 0, self.width(), self.height())
            painter.setPen(QPen(QColor(0x226622)))
            painter.setBrush(Qt.NoBrush)
            painter.drawText(QPoint((self.width() - fm.width("Drop image here")) // 2, self.height() * 3 // 5),
                             "Drop image here")
            painter.setPen(QPen(QColor(0x226622), 4, Qt.DashLine))
            painter.drawRect(0, 0, self.width(), self.height())
        elif self.__state == self.States.wrong_type:
            painter.setPen(QPen(QColor(0xddddaa)))
            painter.setBrush(QBrush(QColor(0xddddaa)))
            painter.drawRect(0, 0, self.width(), self.height())
            painter.setPen(QPen(QColor(0x666622)))
            painter.setBrush(Qt.NoBrush)
            painter.drawText(QPoint((self.width() - fm.width("Wrong image type")) // 2, self.height() * 3 // 5),
                             "Wrong image type")
            painter.setPen(QPen(QColor(0x666622), 4, Qt.DashLine))
            painter.drawRect(0, 0, self.width(), self.height())

    def mouseReleaseEvent(self, event: QMouseEvent) -> None:
        self.__state = self.States.normal
        self.update()
