# in paths.py
import os


class Paths:

    GAME_DATA_DIR = os.path.join(os.getenv("LOCALAPPDATA"), "Larian Studios", "Baldur's Gate 3")
    MOD_LIST_DIR = os.path.join(GAME_DATA_DIR, "Mods")

    ROOT_DIR = os.getcwd()
    DIVINE_FILE = os.path.join(ROOT_DIR, "export_tool", "divine.exe")
    SETTINGS_FILE = os.path.join(ROOT_DIR, "settings.json")
    OUTPUT_DIR = os.path.join(ROOT_DIR, "output")
    TEMP_DIR = os.path.join(ROOT_DIR, "temp")

    # Runesmith paths
    MOD_DIR = "D:\Projects\Mods\Baldurs Gate 3\FFT_WizardTraditions_Runesmith\src"
    UNPACKED_DATA_DIR = "D:\\Apps\\Modding Tools\\Baldurs Gate 3\\BG3 Multitool\\UnpackedData"
    OUTPUT_FILE = "D:\Apps\Modding Tools\Baldurs Gate 3\BG3ModManager\FFT_WizardTraditions_Runesmith.pak"
    ACTION_RESOURCE_DEFINITIONS_FILE = os.path.join(MOD_DIR, "Public", "FFT_WizardTraditions_Runesmith", "ActionResourceDefinitions", "ActionResourceDefinitions.lsx")
    PROGRESSIONS_FILE = os.path.join(MOD_DIR, "Public", "FFT_WizardTraditions_Runesmith", "Progressions", "Progressions.lsx")
    SPELL_LISTS_DB = os.path.join(MOD_DIR, "..", "SpellLists.lsx")
    RUNE_DB = os.path.join(MOD_DIR, "..", "runes.json")
    SHOUT_SPELLS_FILE = os.path.join(MOD_DIR,  "..", "templates", "Spell_Shout.txt")
    # Enum paths.

    ENGLISH_LOCALIZATION_FILE = os.path.join(MOD_DIR, "Localization", "English", "FFT_WizardTraditions_Runesmith.xml")
    ICONS_DIR = os.path.join(MOD_DIR, "Icons")
    OBJECT_FILE = os.path.join(MOD_DIR, "Public", "FFT_WizardTraditions_Runesmith", "Stats", "Generated", "Data", "FFT_Object.txt")
    PROGRESSION_DIR = os.path.join(MOD_DIR, "Progressions")
    ROOT_TEMPLATES_DIR = os.path.join(MOD_DIR, "Public", "FFT_WizardTraditions_Runesmith", "RootTemplates")
    SHOUT_FILE = os.path.join(MOD_DIR, "Public", "FFT_WizardTraditions_Runesmith", "Stats", "Generated", "Data", "FFT_Shout.txt")
    PASSIVE_FILE = os.path.join(MOD_DIR, "Public", "FFT_WizardTraditions_Runesmith", "Stats", "Generated", "Data", "FFT_Passive.txt")
    PASSIVE_LISTS_FILE = os.path.join(MOD_DIR, "Public", "FFT_WizardTraditions_Runesmith", "Lists", "FFT_PassiveLists.lsx")
    SPEll_LISTS_FILE = os.path.join(MOD_DIR, "Public", "FFT_WizardTraditions_Runesmith", "Lists", "FFT_SpellLists.lsx")
