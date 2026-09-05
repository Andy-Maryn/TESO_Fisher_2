"""YetAnotherCompass parser"""
from typing import Optional

from luaParser.yet_another_compass_old.account_wide import AccountWide
from luaParser.common import search
from luaParser.lua_parser import LuaParser


class YetAnotherCompassParser(LuaParser):
    """YetAnotherCompass Parser"""
    lua_file_name: str = 'YetAnotherCompass.lua'

    account_wide: Optional[AccountWide] = None

    size: Optional[int] = None
    left_point: Optional[int] = None
    top_point: Optional[int] = None
    right_point: Optional[int] = None
    bottom_point: Optional[int] = None

    @classmethod
    def load_data(cls) -> None:
        super(YetAnotherCompassParser, cls).load_data()

        cls.account_wide = cls.get_account_wide()

        cls.size = cls.account_wide.size
        cls.left_point = cls.account_wide.position.get('x')
        cls.top_point = cls.account_wide.position.get('y')
        cls.right_point = cls.left_point + cls.size
        cls.bottom_point = cls.top_point + cls.size

    @classmethod
    def get_account_wide(cls) -> AccountWide:
        """Get AccountWide"""
        return AccountWide(search(cls.load_dict, 'AccountWide'))
