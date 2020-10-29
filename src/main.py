import sys

from inline import inline

if len(sys.argv) > 1 and (sys.argv[1] == "inline" or sys.argv[1] == "nogui"):
    inline(sys.argv[2:])
else:
    GuiApp().run()