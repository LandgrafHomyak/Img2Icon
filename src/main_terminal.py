import sys

from inline import inline
from metadata import Metadata

if __name__ == "__main__":
    if len(sys.argv) > 1 and (sys.argv[1] == "inline" or sys.argv[1] == "nogui"):
        inline(sys.argv[2:])
    elif len(sys.argv) > 1 and sys.argv[1] == "info":
        print("Img2Icon (v%d.%d)" % Metadata.version)
    else:
        print("Select option: [inline|nogui|info]")
