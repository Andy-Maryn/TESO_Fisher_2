from dataclasses import dataclass
from typing import Optional

from luaParser.common import set_lua_values


@dataclass
class AccountWide:
    __root: Optional[dict] = None
    __map_for_lua = {
        "position": ("position", dict),
        "centered": ("centered", str),
        "size": ("size", int),
        "compassStyle": ("compassStyle", int),
        "version": ("version", int),
    }

    position: Optional[dict] = None
    centered: Optional[str] = None
    size: Optional[int] = None
    compassStyle: Optional[int] = None
    version: Optional[int] = None

    def __post_init__(self):
        set_lua_values(self, self.__root, self.__map_for_lua)
