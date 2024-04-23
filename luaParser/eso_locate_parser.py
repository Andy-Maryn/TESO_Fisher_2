from typing import Optional

from luaParser.common import search, eso_coordinate_to_screen_position, OBJECT_WIDTH, OBJECT_HEIGHT
from luaParser.lua_parser import LuaParser


class ESOLocateParser(LuaParser):
    """ESO Locate Parser"""
    lua_file_name: str = 'ESOlocate.lua'

    sector: Optional[int] = None
    x_position: Optional[int] = None
    y_position: Optional[int] = None

    left_point: Optional[int] = None
    top_point: Optional[int] = None
    right_point: Optional[int] = None
    bottom_point: Optional[int] = None

    @classmethod
    def load_data(cls) -> None:
        super(ESOLocateParser, cls).load_data()
        eso_locate = cls.get_eso_locate()

        cls.sector = eso_locate.get('3')
        cls.x_position = eso_locate.get('0')
        cls.y_position = eso_locate.get('1')

        cls.left_point, cls.top_point = eso_coordinate_to_screen_position(sector=cls.sector)(
            cls.x_position,
            cls.y_position
        )
        cls.right_point = cls.left_point + OBJECT_WIDTH
        cls.bottom_point = cls.top_point + OBJECT_HEIGHT

    @classmethod
    def get_eso_locate(cls) -> dict:
        return search(cls.load_dict, 'ESOlocate')
