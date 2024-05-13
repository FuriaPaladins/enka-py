from typing import Any, Literal
from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

from ...utils import round_down

from ...constants.hsr import ASCENSION_TO_MAX_LEVEL
from ...constants.hsr import PERCENT_STAT_TYPES
from .icon import CharacterIcon, LightConeIcon
from ...enums.hsr import Element, Path, StatType, RelicType

__all__ = (
    "Trace",
    "Stat",
    "LightCone",
    "RelicSubAffix",
    "Relic",
    "Character",
)


class Trace(BaseModel):
    id: int = Field(alias="pointId")
    level: int

    # Following fields are added in post-processing
    icon: str = Field(None)
    max_level: int = Field(None)
    anchor: str = Field(None)
    type: int = Field(None)


class Stat(BaseModel):
    type: StatType
    value: float

    # Following fields are added in post-processing
    name: str = Field(None)

    @property
    def is_percentage(self) -> bool:
        return self.type.value in PERCENT_STAT_TYPES

    @property
    def formatted_value(self) -> str:
        if self.is_percentage:
            return f"{round_down(self.value * 100, 1)}%"
        else:
            if self.type in {StatType.SPD, StatType.SPEED_DELTA}:
                return str(round_down(self.value, 2))
            return str(int(round_down(self.value, 0)))


class LightCone(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    id: int = Field(alias="tid")
    level: int
    ascension: int = Field(alias="promotion")
    superimpose: int = Field(alias="rank")
    name: str  # Returned as text map hash in the API response
    stats: list[Stat] = Field(alias="props")

    # Following fields are added in post-processing
    icon: LightConeIcon = Field(None)
    rarity: Literal[3, 4, 5] = Field(None)

    @field_validator("name", mode="before")
    def _stringify_name(cls, value: int) -> str:
        return str(value)

    @model_validator(mode="before")
    def _flatten_flat(cls, values: dict[str, Any]) -> dict[str, Any]:
        flat_ = values.pop("_flat")
        values.update(flat_)
        return values


class RelicSubAffix(BaseModel):
    id: int = Field(alias="affixId")
    cnt: int
    step: int | None = None


class Relic(BaseModel):
    id: int = Field(alias="tid")
    level: int
    type: RelicType
    main_affix_id: int = Field(alias="mainAffixId")
    set_name: str = Field(alias="setName")  # Returned as text map hash in the API response
    set_id: int = Field(alias="setID")
    stats: list[Stat] = Field(alias="props")
    sub_affix_list: list[RelicSubAffix] = Field(alias="subAffixList")

    # The following fields are added in post-processing
    icon: str = Field(None)
    rarity: Literal[3, 4, 5] = Field(None)

    @field_validator("set_name", mode="before")
    def _stringify_set_name(cls, value: int) -> str:
        return str(value)

    @model_validator(mode="before")
    def _flatten_flat(cls, values: dict[str, Any]) -> dict[str, Any]:
        flat_ = values.pop("_flat")
        values.update(flat_)
        return values

    @property
    def main_stat(self) -> Stat:
        return self.stats[0]

    @property
    def sub_stats(self) -> list[Stat]:
        return self.stats[1:]


class Character(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    level: int
    ascension: Literal[0, 1, 2, 3, 4, 5, 6] = Field(alias="promotion")
    id: int = Field(alias="avatarId")
    traces: list[Trace] = Field(alias="skillTreeList")
    light_cone: LightCone | None = Field(None, alias="equipment")
    relics: list[Relic] = Field(alias="relicList")
    eidolons_unlocked: int = Field(0, alias="rank")
    is_assist: bool = Field(False, alias="_assist")

    # Following fields are added in post-processing
    icon: CharacterIcon = Field(None)
    name: str = Field(None)
    rarity: Literal[4, 5] = Field(None)
    element: Element = Field(None)
    path: Path = Field(None)
    stats: list[Stat] = Field(list)

    @property
    def max_level(self) -> Literal[20, 30, 40, 50, 60, 70, 80]:
        """Character's max level."""
        return ASCENSION_TO_MAX_LEVEL[self.ascension]
