from enum import Enum


class barbarian_subclass(Enum):
    BERSERKER = {"name": "Berserker", "uuid": ""}
    WILDHEART = {"name": "Wildheart", "uuid": ""}
    WILD_MAGIC = {"name": "Wild Magic", "uuid": ""}


class bard_subclass(Enum):
    COLLEGE_OF_LORE = {"name": "College of Lore", "uuid": ""}
    COLLEGE_OF_VALOR = {"name": "College of Valor", "uuid": ""}
    COLLEGE_OF_SWORDS = {"name": "College of Swords", "uuid": ""}


class wizard_subclass(Enum):
    ABJURATION_SCHOOL = {"name": "Abjuration School", "uuid": "e6a0eb75-7a01-4f40-8563-24ba2615e99b"}
    CONJURATION_SCHOOL = {"name": "Conjuration School", "uuid": "c059dca1-c17d-4dce-8260-83ede5070eac"}
    DIVINATION_SCHOOL = {"name": "Divination School", "uuid": "fbb8347b-20e3-4846-ba91-0552cd12fc5f"}
    ENCHANTMENT_SCHOOL = {"name": "Enchantment School", "uuid": "7a3feb8d-dda7-46ec-9029-1f302f537432"}
    EVOCATION_SCHOOL = {"name": "Evocation School", "uuid": "46d31950-6917-444e-ac87-706702825215"}
    ILLUSION_SCHOOL = {"name": "Illusion School", "uuid": "7577b0e1-a517-4f82-8f72-05a227dc5e88"}
    NECROMANCY_SCHOOL = {"name": "Necromancy School", "uuid": "436c9e1a-3a39-48dd-b753-7cee1bd19c00"}
    TRANSMUTATION_SCHOOL = {"name": "Transmutation School", "uuid": "a12f2924-30b4-4185-9db9-2c5b383ff449"}
