import os
import shutil

from PyInstaller.__main__ import run as build

print("Building: gui_multifile")
build([
    "--onefile",
    "--windowed",
    "--name=gui_multifile",
    "--icon=./resources/icon.ico",
    "./src/main.py"
])

print()
print("Building: terminal")
build([
    "--onefile",
    "--console",
    "--name=terminal",
    "--icon=./resources/icon.ico",
    "./src/main_terminal.py"
])

print()
print("Grouping files")

try:
    os.mkdir("bin")
except FileExistsError:
    pass

shutil.copy("./dist/gui_multifile.exe", "./bin/gui_multifile.exe")
shutil.copy("./dist/terminal.exe", "./bin/terminal.exe")

print("Built successful")