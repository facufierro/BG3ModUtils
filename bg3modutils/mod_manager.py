import os
import re
# from utils.item_manager import ItemManager
from utils.file_manager import FileManager
from utils.paths import Paths
from utils.lslib import LSLib
from model.rune import Rune
from model.spell import Spell
from typing import List, Dict, Tuple
from utils.debug import Log


class RuneList:
    def __init__(self, uuid: str, level: int, runes: List[Rune], handle: str) -> None:
        self.uuid = uuid
        self.level = level
        self.handle = handle
        self.runes = runes
        self.shouts = []


class ModManager:
    def __init__(self):
        try:
            Log.loading("Initializing ModManager")
            spell_ids = ['11f331b0-e8b7-473b-9d1f-19e8e4178d7d', '80c6b070-c3a6-4864-84ca-e78626784eb4']
            handles = ['hb81d7941gbf65g49ddg8232g89fa7f275d75', 'h148ff192gea16g4274gaa3agc27febe1242b']
            self.rune_lists: List[RuneList] = []
            # for each spell id in spell_ids add a RuneList to rune_lists

            # Get the spell files
            spell_files = Spell.get_spell_files()
            # Get the spell data from the files
            spells_from_files = Spell.get_spells_from_files(spell_files)
            # Get the spell lists

            spell_lists = Spell.generate_spell_lists(spells_from_files, spell_ids)
            # Remove duplicates
            unique_spell_ids = set()
            spell_lists = [[spell for spell in sublist if not (spell.id in unique_spell_ids or unique_spell_ids.add(spell.id))] for sublist in spell_lists]
            # Generate the runes

            for index, spell_list in enumerate(spell_lists):
                level = index + 1
                spell_id = spell_ids[index]
                handle = handles[index]
                rune_list = RuneList(spell_id, level, Rune.generate_runes(spell_list), handle)
                self.rune_lists.append(rune_list)

            # Sort the rune lists
            self.rune_lists = [RuneList(rune_list.uuid, rune_list.level, sorted(rune_list.runes, key=lambda rune: rune.spell_name.lower()), rune_list.handle) for rune_list in self.rune_lists]

            # Generate the full rune list
            self.full_rune_list: List[Rune] = []
            for rune_list in self.rune_lists:
                self.full_rune_list.extend(rune_list.runes)

            Log.success("ModManager initialized")
        except Exception as e:
            Log.error(f"Error initializing ModManager: {e}")

    def generate_localization_files(self):
        try:
            Log.info("Generating localization file")
            content_list = []
            # Add the header
            content_list.append(
                f'<?xml version="1.0" encoding="utf-8"?>\n'
                f'<contentList>\n'
                f'<!-- Runesmith -->\n'
                f'<content contentuid="h0d3b68c7g73bcg4e09g81c0g9bab76c77422" version="1">Runesmith</content>\n'
                f'<content contentuid="h8fb5731eg4b5fg4dceg88b1g5069a1f3d9a2" version="1">The Runesmith Tradition, often passed down through dwarven lineages, is a blending of ancient craftsmanship with arcane study. Rooted in the rich heritage of dwarven clans, wizards of this tradition believe that true power lies in the careful inscription of runes, allowing them to bind and harness magic in tangible forms.</content>\n'
                f'<!-- Engrave Weapon -->\n'
                f'<content contentuid="h79246943g1798g4af3ga056gfa31520ade6f" version="2">Engrave Weapon</content>\n'
                f'''<content contentuid="h900117acg8ffbg4cdfgb5fcgf5d9c660b61c" version="4">Engrave a Rune of Power into your main hand weapon. Its damage becames magical and you became &lt;LSTag Tooltip="WeaponProficiency"&gt;Proficient&lt;/LSTag&gt; with it if you weren't already.</content>\n'''
                f'<content contentuid="h5ec98a73g9f51g4fb9gace8g752c13bcf53a" version="2">The weapon returns to your hand if thrown.</content>\n'
                f'<content contentuid="h2700e14fg41deg4634g81b7g609ce01a0edf" version="1">Runic Weapon</content>\n'
                f'''<content contentuid="h7098edf3gd688g4c51g9ef8gd71a36a22f7d" version="3">The wielder of this weapon is always &lt;LSTag Tooltip="Proficiency"&gt;Proficient&lt;/LSTag&gt; with it. The weapon's damage is magical.</content>\n'''
                f'<!-- Rune Carving -->\n'
                f'<content contentuid="hb81d7941gbf65g49ddg8232g89fa7f275d75" version="1">Rune Carving I</content>\n'
                f'<content contentuid="h148ff192gea16g4274gaa3agc27febe1242b" version="1">Rune Carving II</content>\n'
                f'<content contentuid="hd29591e9g6e4dg4596g96e8gd3478ae319dd" version="1">Bind a spell into a piece of stone in the form of a Rune.The Rune can be later activated to cast the spell, it will be consumed on use.</content>\n'
                f'<content contentuid="hb81d7941gbf65g49ddg8232g89fa7f275d75" version="1">Rune Carving I</content>\n'
                f'<!-- Runic Power -->\n'
                f'<content contentuid="h9bc7236dg6bf6g40d1gba60g579e52973e9a" version="1">Runic Power</content>\n'
                f'<content contentuid="hc0453594g11fag475agbbccg5b5891d37556" version="1">Used to carve Runes</content>\n'
                f'<!-- Runic Empowerment -->\n'
                f'<content contentuid="h00be990bgc5c8g4449g9f2bg6bf926c3e4f7" version="3">Runic Empowerment</content>\n'
                f'''<content contentuid="h148ca359gba56g480fg9ff1g5af1cb9e3688" version="6">&lt;LSTag Tooltip="Cantrip"&gt;Cantrips&lt;/LSTag&gt; that cost an action cost a bonus action instead. This effect can only be used while a Runic Weapon is equiped.</content>\n'''
                f'<!-- Runes -->\n')
            # Rune Strings
            rune: Rune
            for rune in self.full_rune_list:
                if not re.search(r'\d$', str(rune.spell.id)):
                    content_list.append(rune.localization_string())

            # Add the footer
            content_list.append(
                '</contentList>\n'
            )
            # Write the file
            destination_file = os.path.join(Paths.ENGLISH_LOCALIZATION_FILE.replace('.xml', '.loca'))
            FileManager.write_file(Paths.ENGLISH_LOCALIZATION_FILE, content_list)
            # Convert the file
            LSLib.execute_command('convert-loca', Paths.ENGLISH_LOCALIZATION_FILE, destination_file)
            Log.success("Localization generated")
        except Exception as e:
            Log.error(f"Error generating localization: {e}")

    def generate_object_file(self):
        try:
            Log.loading("Generating object file")
            content_list = []
            rune: Rune
            for rune in self.full_rune_list:
                content_list.append(rune.object_string())
            FileManager.write_file(Paths.OBJECT_FILE, content_list)
            Log.success("Object file generated")
        except Exception as e:
            Log.error(f"Error generating object: {e}")

    def generate_shout_file(self):
        try:
            Log.loading("Generating base shouts")
            content_list = []
            # Engrave Weapon
            content_list.append(
                f'// Engrave Weapon\n'
                f'new entry "FFT_Shout_EngraveWeapon"\n'
                f'type "SpellData"\n'
                f'data "SpellType" "Shout"\n'
                f'data "SpellProperties" "ApplyEquipmentStatus(MainHand, FFT_RUNIC_WEAPON,100, -1);ApplyStatus(FFT_ENGRAVED_WEAPON,100, -1)"\n'
                f'data "TargetConditions" "Self()"\n'
                f'data "Icon" "FFT_Icon_WeaponEngraving"\n'
                f'data "DisplayName" "h79246943g1798g4af3ga056gfa31520ade6f;2"\n'
                f'data "Description" "h900117acg8ffbg4cdfgb5fcgf5d9c660b61c;4"\n'
                f'data "ExtraDescription" "h5ec98a73g9f51g4fb9gace8g752c13bcf53a;2"\n'
                f'data "TooltipStatusApply" "ApplyStatus(FFT_RUNIC_WEAPON,100, -1)"\n'
                f'data "CastSound" "Action_Cast_BindPactWeapon"\n'
                f'data "CastTextEvent" "Cast"\n'
                f'data "UseCosts" "ActionPoint:1"\n'
                f'data "SpellAnimation" "8b8bb757-21ce-4e02-a2f3-97d55cf2f90b,,;,,;35b644cf-5c13-4407-9dc1-23bf4309216e,,;823e3ddf-c670-41ef-b7b4-9f4a4e38300b,,;7bb52cd4-0b1c-4926-9165-fa92b75876a3,,;,,;0b07883a-08b8-43b6-ac18-84dc9e84ff50,,;,,;,,"\n'
                f'data "VerbalIntent" "Utility"\n'
                f'data "SpellAnimationIntentType" "Aggressive"\n'
                f'data "Requirements" "!Combat"\n'
                f'data "RequirementConditions" "not Unarmed() and not Tagged("PACT_OF_THE_BLADE",GetActiveWeapon())"\n'
                f'data "PrepareEffect" "8e9914c9-7008-4252-ab31-a9776c444194"\n'
                f'data "CastEffect" "fc23a5a6-f05b-40c3-8e0f-99377cfb04cc"\n'
                f'data "Sheathing" "Melee"\n'
                '\n'
                '//Rune Carving\n'
            )
            # Shout_CarveRune
            for rune_list in self.rune_lists:
                runes = rune_list.runes
                for rune in runes:
                    if not re.search(r'\d$', rune.spell_name):
                        rune_list.shouts.append(f"FFT_Shout_CarveRune_{rune.spell_name}")
                shout_list = ";".join(rune_list.shouts)
                base_rune_carving_shout = (
                    f'new entry "FFT_Shout_CarveRune_{rune_list.level}"\n'
                    'type "SpellData"\n'
                    'data "Level" "1"\n'
                    'data "SpellType" "Shout"\n'
                    f'data "ContainerSpells" "{shout_list}"\n'
                    'data "TargetConditions" "Self()"\n'
                    'data "Icon" "FFT_Icon_RuneCarving"\n'
                    f'data "DisplayName" "{rune_list.handle};2"\n'
                    'data "Description" "hd29591e9g6e4dg4596g96e8gd3478ae319dd;2"\n'
                    'data "CastSound" "Action_Cast_PactOfTheBlade"\n'
                    'data "CastTextEvent" "Cast"\n'
                    'data "SpellAnimation" "6f42f5f3-7a5a-4441-a02e-71b0450ac4b7,,;,,;605d49b4-03b9-47f6-96e9-7f80e6be7514,,;fbf20742-9dbf-475b-9ff5-42e4b08064ad,,;42aaefdc-cf9b-4249-b159-285041851f69,,;,,;20e11c98-fff9-4417-88de-5bcc2368a1bd,,;,,;,,"\n'
                    'data "VerbalIntent" "Summon"\n'
                    'data "SpellStyleGroup" "Class"\n'
                    'data "SpellFlags" "IsSpell;IsLinkedSpellContainer"\n'
                    'data "PrepareEffect" "739617e8-1255-4429-8b96-cc86296e0366"\n'
                    'data "CastEffect" "23d05225-027b-4656-97f8-564b185d37a2"\n'
                    'data "DamageType" "Psychic"\n'
                    'data "Sheathing" "Sheathed"\n'
                    '\n'
                )
                content_list.append(base_rune_carving_shout)

            # Empowered Shout_CarveRune

            for rune_list in self.rune_lists:
                for level in range(2, 7):
                    # Empowered Shout_CarveRune Spells
                    empowered_shout_list = []
                    for shout in rune_list.shouts:
                        shout = shout + f"_{level}"
                        empowered_shout_list.append(shout)
                    empowered_shout_list = ";".join(empowered_shout_list)
                    # Empowered Shout_CarveRune
                    content_list.append(
                        f'new entry "FFT_Shout_CarveRune_{rune_list.level}_{level}"\n'
                        'type "SpellData"\n'
                        'data "SpellType" "Shout"\n'
                        f'using "FFT_Shout_CarveRune_{rune_list.level}"\n'
                        f'data "ContainerSpells" "{empowered_shout_list}"\n'
                        f'data "RootSpellID" "FFT_Shout_CarveRune_{rune_list.level}"\n'
                        f'data "PowerLevel" "{level}"\n'
                        '\n'
                    )
            Log.success("Base shouts generated")
            Log.loading("Generating rune carving shouts")

            # CarveRune Spells
            try:
                for rune_list in self.rune_lists:
                    for rune in rune_list.runes:
                        if rune.spell.PowerLevel == None:
                            content_list.append(rune.base_shout_string(rune_list.level))
                        else:
                            content_list.append(rune.powered_shout_string(rune_list.level))
                        # Log.debug(f"Carve Rune Spell generated for {rune.spell_name} power {rune.spell.PowerLevel}")
            except Exception as e:
                Log.error(f"Error generating Carve Rune Spells: {e}")
            # Result String
            FileManager.write_file(Paths.SHOUT_FILE, content_list)

            Log.success("Rune carving shouts generated")
            Log.success("Shout file generated")
        except Exception as e:
            Log.error(f"Error generating shout: {e}")

    def generate_root_templates_files(self):
        try:
            Log.loading("Generating root templates")
            FileManager.clean_folder(Paths.ROOT_TEMPLATES_DIR)
            rune: Rune
            for rune in self.full_rune_list:
                root_template_file = os.path.join(Paths.ROOT_TEMPLATES_DIR, f"rune_{rune.spell_name.lower()}")
                lsx_file = root_template_file + '.lsx'
                lsf_file = root_template_file + '.lsf'

                FileManager.create_file(lsx_file)
                FileManager.write_file(lsx_file, [rune.root_template_string()])
                LSLib.execute_command('convert-resource', lsx_file, lsf_file)
                Log.info(f"Root template generated for {rune.spell_name}")
                FileManager.delete_file(lsx_file)
            Log.success("Root templates generated")
        except Exception as e:
            Log.error(f"Error generating root templates: {e}")

    def pack_mod(self):
        Log.loading("Packing mod...")
        LSLib.execute_command('create-package', Paths.MOD_DIR, Paths.OUTPUT_FILE)
        Log.success("Mod packed")
