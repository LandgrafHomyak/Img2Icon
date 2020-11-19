from enum import IntEnum, auto

from PyQt5.QtCore import QPoint, Qt, QMimeData
from PyQt5.QtGui import QPaintEvent, QPainter, QFont, \
    QFontMetrics, QPen, QColor, QBrush
from PyQt5.QtWidgets import QWidget, QPushButton, QGridLayout, QFrame, QFileDialog

from _old.storage import FileDialogInput, DragAndDropInput


class InputAreaBase(QFrame):
    __slots__ = ("__request_uploading", "__layout", "__drop_area", "__dialog_button")

    def __init__(self, parent, request_uploading):
        super().__init__(parent=parent)

        self.__request_uploading = request_uploading

        self.__layout = QGridLayout(self)
        self.setLayout(self.__layout)

        self.__drop_area = DropImage(self, request_uploading, self._drop_check)
        self.__layout.addWidget(self.__drop_area, 0, 0)

        self.__dialog_button = QPushButton("Select file", self)
        self.__dialog_button.clicked.connect(self.file_dialog)
        self.__layout.addWidget(self.__dialog_button, 1, 0)

    def file_dialog(self, input):
        self.__request_uploading(input)


class DropImage(QWidget):
    class States(IntEnum):
        normal = auto()
        expected_type = auto()
        wrong_drop_type = auto()
        single_link_required = auto()

    __slots__ = ("__state", "__request_uploading", "__check")

    possible_mime_types = (
        "image/jpeg",
        "image/pjpeg",
        "image/png",
        "image/svg+xml",
        "image/tiff",
        "image/vnd.microsoft.icon"
    )

    # on_drop = pyqtSignal(object)

    def __init__(self, parent, request_uploading, check):
        super().__init__(parent)
        self.setAcceptDrops(True)
        self.__request_uploading = request_uploading
        self.__state = self.States.normal
        self.__check = check

    def dragEnterEvent(self, event):
        event.acceptProposedAction()
        self.__state = self.__check(event.mimeData())
        self.update()

    def dragLeaveEvent(self, event):
        self.__state = self.States.normal
        self.update()

    def dropEvent(self, event):
        self.__state = self.States.normal
        self.update()

        event.acceptProposedAction()
        if self.__check(event.mimeData()):
            self.__request_uploading(DragAndDropInput(event.mimeData()))

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
        elif self.__state == self.States.wrong_drop_type:
            painter.setPen(QPen(QColor(0xddddaa)))
            painter.setBrush(QBrush(QColor(0xddddaa)))
            painter.drawRect(0, 0, self.width(), self.height())
            painter.setPen(QPen(QColor(0x666622)))
            painter.setBrush(Qt.NoBrush)
            painter.drawText(QPoint((self.width() - fm.width("Wrong image type")) // 2, self.height() * 3 // 5),
                             "Wrong image type")
            painter.setPen(QPen(QColor(0x666622), 4, Qt.DashLine))
            painter.drawRect(0, 0, self.width(), self.height())
        elif self.__state == self.States.single_link_required:
            painter.setPen(QPen(QColor(0xddddaa)))
            painter.setBrush(QBrush(QColor(0xddddaa)))
            painter.drawRect(0, 0, self.width(), self.height())
            painter.setPen(QPen(QColor(0x666622)))
            painter.setBrush(Qt.NoBrush)
            painter.drawText(QPoint((self.width() - fm.width("Too many links or files")) // 2, self.height() * 3 // 5),
                             "Too many links or files")
            painter.setPen(QPen(QColor(0x666622), 4, Qt.DashLine))
            painter.drawRect(0, 0, self.width(), self.height())

    def mouseReleaseEvent(self, event):
        self.__state = self.States.normal
        self.update()


class InputArea:
    class Single(InputAreaBase):
        def file_dialog(self):
            super().file_dialog(FileDialogInput(QFileDialog.getOpenFileName(self)[0]))

        def _drop_check(self, data: QMimeData):
            if data.hasUrls():
                if len(data.urls()) > 1:
                    return DropImage.States.single_link_required
                else:
                    return DropImage.States.expected_type
            else:
                return DropImage.States.wrong_drop_type

    class Multi(InputAreaBase):
        def file_dialog(self):
            super().file_dialog(FileDialogInput(QFileDialog.getOpenFileNames(self)[0]))

        def _drop_check(self, data: QMimeData):
            if data.hasUrls():
                return DropImage.States.expected_type
            else:
                return DropImage.States.wrong_drop_type
