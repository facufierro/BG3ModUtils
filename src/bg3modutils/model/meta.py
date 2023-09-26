class Meta:
    def __init__(self, uuid: str = None, version: str = None, name: str = None, author: str = None, description: str = None, folder: str = None) -> None:
        self.uuid = uuid
        self.version = version
        self.name = name
        self.author = author
        self.description = description
        self.folder = folder

    def load_from_files(self, meta_file_path: str) -> None:
        pass

    def __str__(self) -> str:
        content = (
            f'<?xml version="1.0" encoding="UTF-8"?>\n'
            f'<save>\n'
            f'<version major="4" minor="0" revision="8" build="612"/>\n'
            f'<region id="Config">\n'
            f'<node id="root">\n'
            f'<children>\n'
            f'<node id="Dependencies"/>\n'
            f'<node id="ModuleInfo">\n'
            f'<attribute id="UUID" type="FixedString" value="080edc42-9ec0-446f-a9c2-792d5bdf4686"/>\n'
            f'<attribute id="Version64" type="int64" value="36169534507319296"/>\n'
            f'<attribute id="Name" type="LSString" value="FFT_WizardTraditions_Runesmith"/>\n'
            f'<attribute id="Author" type="LSString" value="fierrof"/>\n'
            f'<attribute id="Description" type="LSString" value="Adds the Runesmith Wizard subclass to the game."/>\n'
            f'<attribute id="Folder" type="LSString" value="FFT_WizardTraditions_Runesmith"/>\n'
            f'<attribute id="CharacterCreationLevelName" type="FixedString" value=""/>\n'
            f'<attribute id="LobbyLevelName" type="FixedString" value=""/>\n'
            f'<attribute id="MD5" type="LSString" value=""/>\n'
            f'<attribute id="MainMenuBackgroundVideo" type="FixedString" value=""/>\n'
            f'<attribute id="MenuLevelName" type="FixedString" value=""/>\n'
            f'<attribute id="NumPlayers" type="uint8" value="4"/>\n'
            f'<attribute id="PhotoBooth" type="FixedString" value=""/>\n'
            f'<attribute id="StartupLevelName" type="FixedString" value=""/>\n'
            f'<attribute id="Tags" type="LSString" value=""/>\n'
            f'<attribute id="Type" type="FixedString" value="Add-on"/>\n'
            f'<children>\n'
            f'<node id="PublishVersion">\n'
            f'<attribute id="Version64" type="int64" value="36169534507319296"/>\n'
            f'</node>\n'
            f'<node id="TargetModes">\n'
            f'<children>\n'
            f'<node id="Target">\n'
            f'<attribute id="Object" type="FixedString" value="Story"/>\n'
            f'</node>\n'
            f'</children>\n'
            f'</node>\n'
            f'</children>\n'
            f'</node>\n'
            f'</children>\n'
            f'</node>\n'
            f'</region>\n'
            f'</save>\n'
        )
        return content
