from typing import Callable, Union, NoReturn

from PyQt5.QtWidgets import QFrame, QGridLayout, QWidget

from _old.gui.file_managment import FilesList, HasFilesListWidget
from _old.gui.file_managment import InputArea
from _old.storage import FileDialogInput, DragAndDropInput, InputEntity


class FileManager(QFrame, HasFilesListWidget):
    __layout: QGridLayout = ...
    __input_area: InputArea = ...
    __files_list: FilesList = ...

    def __init__(self, parent: QWidget,
                 request_uploading: Callable[[Union[FileDialogInput, DragAndDropInput, InputEntity]], NoReturn],
                 set_selected_slot_number: Callable[[int], NoReturn]): ...

    def files_list_widget(self) -> FilesList: ...
