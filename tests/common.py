from pathlib import Path

import numpy as np
import pytest
from PIL import Image

from luaParser.eso_locate_parser import ESOLocateParser
from luaParser.lua_parser import LuaParser
from luaParser.yet_another_compass_parser import YetAnotherCompassParser
from matrix.destination import Destination
from screenCapture.eso_locate_capture import ESOLocateCapture
from screenCapture.yet_another_compass_capture import YetAnotherCompassCapture

CAPTURE_PATH = Path(r"C:\Users\Andy\PycharmProjects\tesoFisher\tests\data_screen_capture")
ESO_LOCATE_CAPTURE_PATH = CAPTURE_PATH / Path("locate")


@pytest.fixture(scope="session")
def data_path():
    LuaParser._root = Path(r'C:\Users\Andy\PycharmProjects\tesoFisher\tests\lua')
    Destination._root = Path(r'C:\Users\Andy\PycharmProjects\tesoFisher\tests\matrix')
    yield
    LuaParser._root = Path('C:/Users/Andy/Documents/Elder Scrolls Online/live/SavedVariables')
    Destination._root = Path(r'C:\Users\Andy\PycharmProjects\tesoFisher\matrix')


@pytest.fixture(scope="session", autouse=True)
def load_data(data_path):
    ESOLocateParser.load_data()
    ESOLocateParser.set_user_property('BendreTolstyy')

    YetAnotherCompassParser.load_data()

    Destination.load_data()


@pytest.fixture
def eso_locate_capture(request):
    with Image.open(ESO_LOCATE_CAPTURE_PATH / request.param) as img:
        img.load()
    ESOLocateCapture.capture = np.array(
        img.crop((ESOLocateParser.left_point,
                  ESOLocateParser.top_point,
                  ESOLocateParser.right_point,
                  ESOLocateParser.bottom_point))
    )[:, 100:200, :]
    ESOLocateCapture.segmentation_test()


@pytest.fixture
def yet_another_compass_capture(request):
    with Image.open(CAPTURE_PATH / request.param) as img:
        img.load()
    YetAnotherCompassCapture.capture = np.array(
        img.crop((YetAnotherCompassParser.left_point,
                  YetAnotherCompassParser.top_point,
                  YetAnotherCompassParser.right_point,
                  YetAnotherCompassParser.bottom_point))
    )
    YetAnotherCompassCapture.segmentation_test(25)
