from PyQt5.QtSvg import QSvgRenderer
from PyQt5.QtXml import QDomDocument


class Svg:
    __slots__ = ("__dom", "__renderer")

    def __init__(self, path):
        self.__dom = QDomDocument()
        with open(path) as fistream:
            self.__dom.setContent(fistream.read())

        self.__renderer = QSvgRenderer(self.__dom.toByteArray())

    @property
    def dom(self):
        return self.__dom

    @property
    def renderer(self):
        return self.__renderer
