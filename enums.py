from enum import Enum
from utils.paths import Paths


class FileType(Enum):
    ENGLISH_LOCALIZATION = Paths.ENGLISH_LOCALIZATION_FILE
    ICONS = Paths.ICONS_DIR
    OBJECT = Paths.OBJECT_FILE
    PROGRESSION = Paths.PROGRESSION_DIR
    ROOT_TEMPLATES = Paths.ROOT_TEMPLATES_DIR
    SHOUT = Paths.SHOUT_FILE
