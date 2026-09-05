"""User"""
from dataclasses import dataclass
from typing import Optional

from luaParser.common import set_lua_values


@dataclass
class AccountWide:
    """AccountWide"""
    __root: Optional[dict] = None
    __map_for_lua = {
        "off_set_x": ("offSetX", int),
        "off_set_y": ("offSetY", int),
        "point": ("point", int),
        "relative_point": ("relativePoint", int),
    }

    off_set_x: Optional[int] = None
    off_set_y: Optional[int] = None
    point: Optional[int] = None
    relative_point: Optional[int] = None

    def __post_init__(self):
        set_lua_values(self, self.__root, self.__map_for_lua)
