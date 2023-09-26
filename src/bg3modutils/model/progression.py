from typing import List


class Progression:

    def __init__(self, uuid: str = None, name: str = None, level: int = None, table_uuid: str = None, progression_type: str = None, boosts: list = None, passives_added: list = None, passives_removed: list = None, selectors: list = None, is_multiclass: bool = None) -> None:
        uuid = uuid
        name = name
        level = level
        table_uuid = table_uuid
        progression_type = progression_type
        boosts = boosts
        passives_added = passives_added
        passives_removed = passives_removed
        selectors = selectors
        is_multiclass = is_multiclass

    @classmethod
    def progressions_string(cls, progressions_list: List['Progression']) -> str:
        content = []
        for progression in progressions_list:
            content.append(str(progression))
        return "\n".join(content)

    @classmethod
    def load_progressions_from_file(cls, file_path: str) -> None:
        progression_list = []
        return progression_list

    def __str__(self) -> str:
        content = (
            ""
        )
        return content
