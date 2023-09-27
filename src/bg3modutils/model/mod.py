from typing import List
from bg3modutils.model.meta import Meta
from bg3modutils.model.progression import Progression
from bg3modutils.utils.lslib import LSLib
from bg3modutils.utils.debug import Log


class Mod:
    def __init__(self, meta: Meta = None, progressions: List[Progression] = None) -> None:
        try:
            self.meta = meta
            self.progressions = progressions
        except Exception as e:
            Log.error(f"Failed to initialize Mod: {e}")
