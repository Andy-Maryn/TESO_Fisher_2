"""User"""
from dataclasses import dataclass
from typing import Optional

from luaParser.common import set_lua_values


@dataclass
class ESOLocate:
    """ESOLocate"""
    __root: Optional[dict] = None
    __map_for_lua = {
        "x_position": ("0", int),
        "y_position": ("1", int),
        "sector": ("2", int),
        "sector2": ("3", int),
        "version": ("version", int),
    }

    x_position: Optional[int] = None
    y_position: Optional[int] = None
    sector: Optional[int] = None
    sector2: Optional[int] = None
    version: Optional[int] = None

    def __post_init__(self):
        set_lua_values(self, self.__root, self.__map_for_lua)
