from typing import List
from model.meta import Meta
from model.progression import Progression
from utils.lslib import LSLib


class Mod:
    def __init__(self, meta: Meta = None, progressions: List[Progression] = None) -> None:
        self.meta = meta
        self.progressions = progressions
