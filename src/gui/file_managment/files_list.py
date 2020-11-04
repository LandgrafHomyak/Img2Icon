from enum import IntEnum, auto

from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QImage, QPaintEvent, QPainter, QPen, QColor, QBrush
from PyQt5.QtWidgets import QTableWidget, QAbstractItemView, QLabel, QWidget, QPushButton


class FilesList(QTableWidget):
    __slots__ = ("__rows", "__set_selected_slot_number")

    def __init__(self, parent, set_selected_slot_number):
        super().__init__(parent=parent)
        self.__rows = []
        self.setColumnCount(4)
        self.setHorizontalHeaderLabels(["Preview", "State", "Type", "Delete"])
        self.clicked.connect(self.row_clicked)
        self.setFocusPolicy(Qt.NoFocus)
        self.setSelectionMode(QAbstractItemView.NoSelection)
        self.__set_selected_slot_number = set_selected_slot_number

    def delete_row(self, row_object):
        y = self.__rows.index(row_object)
        if y == -1:
            pass
        else:
            self.removeRow(y)
            self.__rows.pop(y)

    def add_rows(self, count, callback=None):
        self.setRowCount(len(self.__rows) + count)
        for y in range(len(self.__rows), len(self.__rows) + count):
            self.__rows.append(Row())
            self.init_row(y)
        if callback is not None:
            callback()

    def get_row(self, y):
        return self.__rows[y]

    def init_row(self, y):
        row = self.__rows[y]

        row.preview = ImagePreview(self)
        self.setCellWidget(y, 0, row.preview)

        row.state = UploadingState(self)
        self.setCellWidget(y, 1, row.state)

        row.format = QLabel(self)
        self.setCellWidget(y, 2, row.format)

        row.delete_btn = DeleteButton(self)
        self.setCellWidget(y, 3, row.delete_btn)

    def row_clicked(self, event):
        self.__set_selected_slot_number(event.row())

    def __len__(self):
        return len(self.__rows)


class Row:
    __slots__ = ("preview", "state", "format", "delete_btn")

    def __init__(self):
        self.preview = None
        self.state = None
        self.format = None
        self.delete_btn = None


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


class DeleteButton(QPushButton):
    def __init__(self, parent):
        super().__init__(parent=parent)


class UploadingState(QWidget):
    class States(IntEnum):
        not_stated = auto()
        in_order = auto()
        processing = auto()
        complete = auto()
        error = auto()

    __slots__ = ("__state",)

    def __init__(self, parent):
        super().__init__(parent=parent)
        self.__state = self.States.not_stated
        self.update()

    def in_order(self):
        self.__state = self.States.in_order
        self.update()

    def processing(self):
        self.__state = self.States.processing
        self.update()

    def complete(self):
        self.__state = self.States.complete
        self.update()

    def error(self):
        self.__state = self.States.error
        self.update()

    def paintEvent(self, event: QPaintEvent):
        painter = QPainter(self)
        cx = self.width() // 2
        cy = self.height() // 2
        r = min(cx, cy) - 2
        if self.__state == self.States.not_stated:
            painter.setPen(QPen(QColor(0x666666)))
            painter.setBrush(QBrush(QColor(0xaaaaa)))
            painter.drawRect(cx - r, cy - r, r * 2, r * 2)
        elif self.__state == self.States.in_order:
            painter.setPen(QPen(QColor(0x008fdd)))
            painter.setBrush(QBrush(QColor(0x008fdd)))
            painter.drawRect(cx - r, cy - min(1, r // 5), r * 2, r * 2 // 5)
            painter.drawEllipse(cx - r // 2, cy - r // 2, r, r)
        elif self.__state == self.States.processing:
            painter.setPen(QPen(QColor(0x00df81)))
            painter.setBrush(QBrush(QColor(0x00df81)))
            painter.drawEllipse(cx - r, cy - r, r * 2, r * 2)
            painter.setPen(QPen(QColor(0xffffff)))
            painter.setBrush(QBrush(QColor(0xffffff)))
            painter.drawEllipse(cx - r // 2, cy - r // 2, r, r)
        elif self.__state == self.States.complete:
            painter.setPen(QPen(QColor(0x00dd00)))
            painter.setBrush(QBrush(QColor(0x00dd00)))
            painter.drawEllipse(cx - r, cy - r, r * 2, r * 2)

        elif self.__state == self.States.error:
            painter.setPen(QPen(QColor(0xdd0000)))
            painter.setBrush(QBrush(QColor(0xdd0000)))
            painter.drawEllipse(cx - r, cy - r, r * 2, r * 2)


class HasFilesListWidget:
    def files_list_widget(self):
        raise NotImplementedError
