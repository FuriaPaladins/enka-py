import sys

if sys.version_info < (3, 11):
    from enum import Enum as StrEnum
else:
    from enum import StrEnum


class Game(StrEnum):
    """Game."""

    GI = "gi"
    HSR = "hsr"
