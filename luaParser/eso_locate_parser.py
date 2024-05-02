from collections.abc import KeysView
from typing import Optional

from luaParser.common import search, eso_coordinate_to_screen_position, OBJECT_WIDTH, OBJECT_HEIGHT
from luaParser.lua_parser import LuaParser
from luaParser.user import ESOLocate


class ESOLocateParser(LuaParser):
    """ESO Locate Parser"""
    lua_file_name: str = 'ESOlocate.lua'

    eso_locate: Optional[dict] = None
    user: Optional[str] = None

    left_point: Optional[int] = None
    top_point: Optional[int] = None
    right_point: Optional[int] = None
    bottom_point: Optional[int] = None

    @classmethod
    def load_data(cls) -> None:
        super(ESOLocateParser, cls).load_data()
        cls.eso_locate = cls.get_eso_locate()

    @classmethod
    def get_eso_locate(cls) -> dict:
        result = {}
        default = search(cls.load_dict, 'Default')
        account = next(iter(default))
        for key, value in default[account].items():
            result[key] = ESOLocate(value.get('ESOlocate'))

        return result

    @classmethod
    def get_users_list(cls) -> KeysView:
        return cls.eso_locate.keys()

    @classmethod
    def set_user_property(cls, user: str):
        cls.user = user
        properties = cls.eso_locate.get(cls.user)

        cls.left_point, cls.top_point = eso_coordinate_to_screen_position(sector=properties.sector)(
            properties.x_position,
            properties.y_position
        )
        cls.right_point = cls.left_point + OBJECT_WIDTH
        cls.bottom_point = cls.top_point + OBJECT_HEIGHT
        pass


