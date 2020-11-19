from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication


def convert(*, src, dst, qapp=None, width=None, height=None):
    temp = False
    if qapp is None:
        qapp = QApplication([])
        temp = True
    img = QIcon(src)
    sizes = img.availableSizes()
    pxmp = img.pixmap(width or sizes[0].width(), height or sizes[0].height())
    result = pxmp.save(dst, "ico")
    if temp:
        qapp.exit(0)
    return result
