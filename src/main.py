from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication

app = QApplication([])
img = QIcon("../resources/icon.png")
pxmp = img.pixmap(256, 256)
if pxmp.save("../resources/icon.ico", "ico"):
    print("Successful")
else:
    print("Error")
