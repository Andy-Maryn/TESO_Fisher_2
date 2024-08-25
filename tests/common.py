import os
from pathlib import Path

import numpy as np
import pytest
import pytest_html
from PIL import Image

from luaParser.eso_locate_parser import ESOLocateParser
from luaParser.lua_parser import LuaParser
from luaParser.yet_another_compass_parser import YetAnotherCompassParser
from matrix.destination import Destination
from screenCapture.eso_locate_capture import ESOLocateCapture
from screenCapture.yet_another_compass_capture import YetAnotherCompassCapture
from tests.conftest import base_image_path, base_image_array

CAPTURE_PATH = Path(__file__).resolve().parents[1] / Path(r"tests/data_screen_capture")
ESO_LOCATE_CAPTURE_PATH = CAPTURE_PATH / Path("locate")
CAPTURE_PATH = Path()


@pytest.fixture(scope="session")
def data_path():
    LuaParser._root = os.path.dirname(os.path.abspath(__file__)) / Path(r'lua')
    Destination._root = os.path.dirname(os.path.abspath(__file__)) / Path(r'matrix')
    yield
    LuaParser._root = Path('C:/Users/Andrii/Documents/Elder Scrolls Online/live/SavedVariables')
    Destination._root = Path(r'C:\Users\Andrii\PycharmProjects\tesoFisher\matrix')


@pytest.fixture(scope="session")
def load_test_data(data_path):
    ESOLocateParser.load_data()
    ESOLocateParser.set_user_property('BendreTolstyy')

    YetAnotherCompassParser.load_data()

    Destination.load_data()

@pytest.fixture(scope="session")
def load_data():
    ESOLocateParser.load_data()
    ESOLocateParser.set_user_property('BendreTolstyy')

    YetAnotherCompassParser.load_data()

    Destination.load_data()


@pytest.fixture
def eso_locate_capture(request, extras):
    extras.append(pytest_html.extras.png(base_image_path(ESO_LOCATE_CAPTURE_PATH / request.param)))

    with Image.open(ESO_LOCATE_CAPTURE_PATH / request.param) as img:
        img.load()
    ESOLocateCapture.capture = np.array(
        img.crop((ESOLocateParser.left_point,
                  ESOLocateParser.top_point,
                  ESOLocateParser.right_point,
                  ESOLocateParser.bottom_point))
    )[5:18, 110:190]
    extras.append(
        pytest_html.extras.image(
            base_image_array(ESOLocateCapture.capture, mode='RGB')
        )
    )
    ESOLocateCapture.segmentation_test(20)


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
