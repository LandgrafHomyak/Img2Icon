from os.path import splitext
from pathlib import Path

from _old.convert import convert


def inline(options):
    args = []
    kwargs = dict()
    for v in options:
        if v.startswith("--"):
            v = v.split("=")
            kwargs[v[0][2:]] = "=".join(v[1:])
        else:
            args.append(v)

    src_name = None
    if len(args) >= 1:
        src_name = args[0]
    if "src" in kwargs:
        src_name = kwargs["src"]
    if src_name is None:
        print("Path to source image doesn't set")
        exit(1)

    dst_name = None
    if len(args) >= 2:
        dst_name = args[1]
    if "dst" in kwargs:
        dst_name = kwargs["dst"]
    if dst_name is None:
        dst_name = splitext(src_name)[0] + ".ico"

    width = None
    if len(args) >= 3:
        width = args[2]
    if "width" in kwargs:
        width = kwargs["width"]
    if "w" in kwargs:
        width = kwargs["w"]
    if width is not None:
        if width.isdigit():
            width = int(width)
        else:
            print("Width must be a number")
            exit(4)

    height = None
    if len(args) >= 4:
        height = args[3]
    if "height" in kwargs:
        height = kwargs["height"]
    if "h" in kwargs:
        height = kwargs["h"]
    if height is not None:
        if height.isdigit():
            height = int(height)
        else:
            print("Height must be a number")
            exit(4)

    noconfirm = "noconfirm" in kwargs

    src_path = Path(src_name)
    if not src_path.exists():
        print("Source image doesn't exists")
        exit(2)
    if not src_path.is_file():
        print("Source path is not a file")
        exit(3)

    dst_path = Path(dst_name)
    if dst_path.exists() and not noconfirm:
        print("Output file already exists, do you want to rewrite it?")
        answer = input("[y/N]: ").strip().lower()
        if not answer.startswith("y"):
            print("Operation aborted")
            exit(0)

    if convert(src=src_name, dst=dst_name, qapp=None, width=width, height=height):
        print("Successful")
    else:
        print("Error")
