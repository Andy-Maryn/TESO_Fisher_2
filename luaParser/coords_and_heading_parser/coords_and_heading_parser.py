"""CoordsAndHeading parser"""
from typing import Optional

from luaParser.common import search, OBJECT_WIDTH, OBJECT_HEIGHT, coords_capture
from luaParser.coords_and_heading_parser.account_wide import AccountWide
from luaParser.lua_parser import LuaParser


# noinspection SpellCheckingInspection
class CoordsAndHeadingParser(LuaParser):
    """Coords And Heading Parser"""
    lua_file_name: str = 'CoordsAndHeading.lua'
    account_wide: Optional[AccountWide] = None

    left_point: Optional[int] = None
    top_point: Optional[int] = None
    right_point: Optional[int] = None
    bottom_point: Optional[int] = None

    @classmethod
    def load_data(cls) -> None:
        super(CoordsAndHeadingParser, cls).load_data()
        cls.account_wide = cls.get_account_wide()

        cls.left_point, cls.top_point = coords_capture(cls.account_wide.off_set_x, cls.account_wide.off_set_y,
                                                       cls.account_wide.point, cls.account_wide.relative_point)
        cls.right_point = cls.left_point + OBJECT_WIDTH
        cls.bottom_point = cls.top_point + OBJECT_HEIGHT

    @classmethod
    def get_account_wide(cls) -> AccountWide:
        """Get AccountWide"""
        return AccountWide(search(cls.load_dict, 'AccountWide'))
