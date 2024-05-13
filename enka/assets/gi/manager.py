from typing import TYPE_CHECKING

from ..data import AssetData
from .file_paths import (
    CHARACTER_DATA_PATH,
    CONSTS_DATA_PATH,
    NAMECARD_DATA_PATH,
    PFPS_DATA_PATH,
    TALENTS_DATA_PATH,
    TEXT_MAP_PATH,
)

if TYPE_CHECKING:
    from ...enums.gi import Language

__all__ = ("AssetManager",)


class AssetManager:
    """Genshin Impact asset manager."""

    def __init__(self, lang: "Language") -> None:
        self._lang = lang
        self.text_map = TextMap(lang)
        self.character_data = CharacterData()
        self.namecard_data = NamecardData()
        self.consts_data = ConstsData()
        self.talents_data = TalentsData()
        self.pfps_data = PfpsData()

    async def load(self) -> bool:
        """Load all assets.

        Returns:
            bool: Whether all assets were loaded successfully.
        """
        text_map_loaded = await self.text_map.load()
        character_data_loaded = await self.character_data.load()
        namecard_data_loaded = await self.namecard_data.load()
        consts_data_loaded = await self.consts_data.load()
        talents_data_loaded = await self.talents_data.load()
        pfp_data_loaded = await self.pfps_data.load()

        return (
            text_map_loaded
            and character_data_loaded
            and namecard_data_loaded
            and consts_data_loaded
            and talents_data_loaded
            and pfp_data_loaded
        )


class TextMap(AssetData):
    def __init__(self, lang: "Language") -> None:
        super().__init__()
        self._lang = lang

    async def load(self) -> bool:
        text_map = await self._open_json(TEXT_MAP_PATH)
        if text_map is not None:
            self._data = text_map[self._lang.value]
        return self._data is not None


class CharacterData(AssetData):
    async def load(self) -> bool:
        self._data = await self._open_json(CHARACTER_DATA_PATH)
        return self._data is not None


class NamecardData(AssetData):
    async def load(self) -> bool:
        self._data = await self._open_json(NAMECARD_DATA_PATH)
        return self._data is not None


class ConstsData(AssetData):
    async def load(self) -> bool:
        self._data = await self._open_json(CONSTS_DATA_PATH)
        return self._data is not None


class TalentsData(AssetData):
    async def load(self) -> bool:
        self._data = await self._open_json(TALENTS_DATA_PATH)
        return self._data is not None


class PfpsData(AssetData):
    async def load(self) -> bool:
        self._data = await self._open_json(PFPS_DATA_PATH)
        return self._data is not None
