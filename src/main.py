import sys

from gui.app import GuiApp
from inline import inline
from metadata import Metadata

if len(sys.argv) > 1 and (sys.argv[1] == "inline" or sys.argv[1] == "nogui"):
    inline(sys.argv[2:])
if len(sys.argv) > 1 and sys.argv[1] == "info":
    print("Img2Icon (v%d.%d)" % Metadata.version)
else:
    GuiApp().run()