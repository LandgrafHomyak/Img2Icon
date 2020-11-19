from time import time

from PyInstaller.__main__ import run as build


start_time = time()
ms = lambda: "% 7s ms" % str(int((time() - start_time) * 1000))

print(f"\033[1m\033[94m\033[4m[{ms()}] Building: 'Convert image to icon.exe'...\033[0m")
try:
    build([
        "--onefile",
        "--windowed",
        "--name=Convert image to icon.exe",
        # "--icon=./resources/icon.ico",
        "./src/main/Convert image to icon.py"
    ])

except:
    print(f"\033[91m[{ms()}] Build failed!\033[0m")
    exit(1)
else:
    print(f"\033[92m[{ms()}] Build successful!\033[0m")

print()
print(f"\033[1m\033[94m\033[4m[{ms()}] Building: 'img2icon.exe'...\033[0m")
try:
    build([
        "--onefile",
        "--windowed",
        "--name=img2icon",
        # "--icon=./resources/icon.ico",
        "./src/main/img2icon.py"
    ])

except:
    print(f"\033[91m[{ms()}] Build failed!\033[0m")
    exit(1)
else:
    print(f"\033[92m[{ms()}] Build successful!\033[0m")
print()
print(f"\033[1m\033[4m\033[92m[{ms()}] All files were built!\033[0m")