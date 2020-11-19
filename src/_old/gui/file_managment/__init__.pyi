from typing import Callable, Union, NoReturn

from PyQt5.QtWidgets import QFrame, QWidget

from _old.storage import FileDialogInput, DragAndDropInput, InputEntity
from .files_list import FilesList


class HasFilesListWidget:
    def files_list_widget(self) -> FilesList: ...


class InputArea(QFrame):
    def __init__(self, parent: QWidget,
                 request_uploading: Callable[
                     [Union[FileDialogInput, DragAndDropInput, InputEntity]], NoReturn]) -> NoReturn: ...


class FileManager(QFrame, HasFilesListWidget):
    def __init__(self, parent: QWidget,
                 request_uploading: Callable[[Union[FileDialogInput, DragAndDropInput, InputEntity]], NoReturn],
                 set_selected_slot_number: Callable[[int], NoReturn]): ...

    def files_list_widget(self) -> FilesList: ...
