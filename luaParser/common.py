"""Lua parser common"""
import ctypes
from enum import Enum
from typing import Any, Callable

user32 = ctypes.windll.user32
user32.SetProcessDPIAware()
WIDTH_SCREEN = user32.GetSystemMetrics(0)
HEIGHT_SCREEN = user32.GetSystemMetrics(1)

OBJECT_WIDTH = 300
OBJECT_HEIGHT = 20

TOP_BOARDS = 0
BOTTOM_BOARDS = 10

HORIZONTAL_BOARDS = 0


class XPosition(Enum):
    """Describe 'x' capture position"""
    left: Callable[[int], int] = lambda x: x + HORIZONTAL_BOARDS
    right: Callable[[int], int] = lambda x: x + WIDTH_SCREEN - (OBJECT_WIDTH + HORIZONTAL_BOARDS)
    mid: Callable[[int], int] = lambda x: x + (WIDTH_SCREEN // 2) - (OBJECT_WIDTH // 2)


class YPosition(Enum):
    """Describe 'y' capture position"""
    top: Callable[[int], int] = lambda y: y + TOP_BOARDS
    bottom: Callable[[int], int] = lambda y: y + HEIGHT_SCREEN - (OBJECT_HEIGHT + BOTTOM_BOARDS)
    mid: Callable[[int], int] = lambda y: y + (HEIGHT_SCREEN // 2) - (OBJECT_HEIGHT // 2)


def eso_coordinate_to_screen_position(sector) -> Callable[[int, int], tuple[int, int]]:
    """Convert EsoLocate coordinates to window coordinates"""
    switch: dict = {
        0: lambda x, y: (XPosition.left(x), YPosition.top(y)),
        1: lambda x, y: (XPosition.mid(x), YPosition.top(y)),
        2: lambda x, y: (XPosition.left(x), YPosition.mid(y)),
        3: lambda x, y: (XPosition.left(x), YPosition.top(y)),
        4: lambda x, y: (XPosition.mid(x), YPosition.bottom(y)),
        5: lambda x, y: (XPosition.left(x), YPosition.top(y)),
        6: lambda x, y: (XPosition.left(x), YPosition.bottom(y)),
        7: lambda x, y: (XPosition.left(x), YPosition.top(y)),
        8: lambda x, y: (XPosition.right(x), YPosition.mid(y)),
        9: lambda x, y: (XPosition.right(x), YPosition.top(y)),
        10: lambda x, y: (XPosition.left(x), YPosition.top(y)),
        11: lambda x, y: (XPosition.left(x), YPosition.top(y)),
        12: lambda x, y: (XPosition.right(x), YPosition.bottom(y)),
    }
    return switch.get(sector)


def search(data: dict, lua_property: str, result: dict = None) -> dict | None:
    """Search data in .lua file"""
    if isinstance(data, dict):
        for key, val in data.items():
            if key == lua_property:
                result = val
            else:
                result = search(val, lua_property, result)
    return result


def set_lua_values(obj: Any, root: dict, mapping: dict[str, tuple]) -> None:
    """Write values from .lua to dataclasses"""
    for prop, value in mapping.items():
        value, to_type = value
        param_value = to_type(root.get(value))
        setattr(obj, prop, param_value)
