"""Lua parser"""
import json
from pathlib import Path


class LuaParser:
    """Lua Parser"""
    # TODO: path to 'Documents' folder should not be hard coded
    _root: Path = Path(r'C:\Users\Andrii\Documents\Elder Scrolls Online\live\SavedVariables')
    lua_file_name: str = ''

    load_dict: dict

    @classmethod
    @property
    def path(cls) -> Path:
        """Path"""
        return cls._root / cls.lua_file_name

    @classmethod
    def load_data(cls) -> None:
        """Load data from .lua and convert to dictionary"""
        with open(cls.path, "r") as file:
            data = str(file.read()) \
                .replace(' ', '') \
                .replace('\n', '') \
                .replace('["', '"') \
                .replace('"]', '"') \
                .replace('@', '') \
                .replace('$', '') \
                .replace('=', ':') \
                .replace(',}', '}') \
                .replace('{[', '{"') \
                .replace(']:', '":') \
                .replace(',[', ',"')  # can be reason of pars fail

            data = data[data.find('{'):]
        cls.load_dict = json.loads(data)
