from PyQt5.QtWidgets import QFrame, QGridLayout

from _old.gui.workspace.widgets import ImagePreview, Output, Resize, AvailableSizes


class Workspace(QFrame):
    def __init__(self, parent):
        super().__init__(parent)

        self.__layout = QGridLayout(self)
        self.setLayout(self.__layout)

        self.__preview = ImagePreview(self)
        self.__layout.addWidget(self.__preview, 0, 0, 1, 1)

        self.__output = Output(self)
        self.__layout.addWidget(self.__output, 1, 0, 1, 1)

        self.__resize = Resize(self)
        self.__layout.addWidget(self.__resize, 2, 0, 1, 1)

        self.__available_sizes = AvailableSizes(self)
        self.__layout.addWidget(self.__available_sizes, 3, 0, 1, 1)

        self.__slot = None

    def set_slot(self, slot):
        self.__slot = slot
        self.__preview.set_prepared_image(slot.prepared)
