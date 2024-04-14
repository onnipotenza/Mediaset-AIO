import os
import ctypes


def padToCenter(l: list, w: int) -> str:
    padding = ' ' * \
        (w//2)
    parts = [padding[0: (w-len(p))//2+1]+p for p in l]
    return '\n'.join(parts)


def logo():
    ctypes.windll.kernel32.SetConsoleTitleW(
        "Mediaset AIO v1.0 | Best Mediaset Downloader")

    os.system('cls' if os.name == 'nt' else 'clear')
    logo = [
        "    __  ___         ___                 __     ___    ________",
        "    /  |/  /__  ____/ (_)___ _________  / /_   /   |  /  _/ __ \\",
        "   / /|_/ / _ \\/ __  / / __ `/ ___/ _ \\/ __/  / /| |  / // / / /",
        "  / /  / /  __/ /_/ / / /_/ (__  )  __/ /_   / ___ |_/ // /_/ / ",
        " /_/  /_/\\___/\\__,_/_/\\__,_/____/\\___/\\__/  /_/  |_/___/\\____/  "
    ]


    print(padToCenter(logo, 55))
    print("")
    print("Version 1.0".center(110))
    print("")
    print("")
    print("")

logo()