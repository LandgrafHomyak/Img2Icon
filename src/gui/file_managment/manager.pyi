from typing import Callable, Union, NoReturn

from PyQt5.QtWidgets import QFrame, QGridLayout, QWidget

from gui.file_managment.files_list import FilesList, HasFilesListWidget
from gui.file_managment.input import InputArea
from storage import FileDialogInput, DragAndDropInput, InputEntity


class FileManager(QFrame, HasFilesListWidget):
    __layout: QGridLayout = ...
    __input_area: InputArea = ...
    __files_list: FilesList = ...

    def __init__(self, parent: QWidget,
                 request_uploading: Callable[[Union[FileDialogInput, DragAndDropInput, InputEntity]], NoReturn],
                 set_selected_slot_number: Callable[[int], NoReturn]): ...

    def files_list_widget(self) -> FilesList: ...
