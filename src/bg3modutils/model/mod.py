from typing import List
from bg3modutils import Meta
from bg3modutils import Progression
from utils.lslib import LSLib


class Mod:
    def __init__(self, meta: Meta = None, progressions: List[Progression] = None) -> None:
        self.meta = meta
        self.progressions = progressions
