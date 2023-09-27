import os


class Paths:
    MODS_DIR = os.path.join(os.getenv('LOCALAPPDATA'), "Larian Studios", "Baldur's Gate 3", "Mods")
    DIVINE_FILE = os.path.join(os.path.dirname(os.path.realpath(__file__)), "ExportTool", "Tools", "divine.exe")
