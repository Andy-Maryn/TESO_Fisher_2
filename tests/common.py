import time
from pathlib import Path

import numpy as np
import pytest
import pytest_html
from pytest_check import check
from PIL import Image

from csvParser.adjacency_matrix import AdjacencyMatrixParser
from definitions import TEST_DIR
from luaParser.eso_locate_parser import ESOLocateParser
from luaParser.lua_parser import LuaParser
from luaParser.yet_another_compass_parser import YetAnotherCompassParser
from matrix.destination import Destination
from moving.rotation.rotation import Rotation
from screenCapture.eso_locate_capture import ESOLocateCapture
from screenCapture.yet_another_compass_capture import YetAnotherCompassCapture
from tests.conftest import base_image_path, base_image_array

CAPTURE_PATH = TEST_DIR / 'data_screen_capture'
ESO_LOCATE_CAPTURE_PATH = CAPTURE_PATH / 'locate'
YET_ANOTHER_COMPASS_CAPTURE_PATH = CAPTURE_PATH / 'compass'


@pytest.fixture(scope="session")
def data_path():
    LuaParser._root = TEST_DIR / 'lua'
    AdjacencyMatrixParser._root = TEST_DIR / 'matrix'
    yield
    LuaParser._root = Path('C:/Users/Andrii/Documents/Elder Scrolls Online/live/SavedVariables')
    AdjacencyMatrixParser._root = TEST_DIR / 'matrix'


@pytest.fixture(scope="session")
def load_test_data(data_path):
    ESOLocateParser.load_data()
    ESOLocateParser.set_user_property('BendreTolstyy')

    YetAnotherCompassParser.load_data()

    AdjacencyMatrixParser.load_data()
    Destination.load_data()

@pytest.fixture(scope="session")
def load_data():
    ESOLocateParser.load_data()
    ESOLocateParser.set_user_property('BendreTolstyy')

    YetAnotherCompassParser.load_data()

    AdjacencyMatrixParser.load_data()
    Destination.load_data()

@pytest.fixture
def screen_is_ready(extras):
    start_time = time.time()
    current_time = time.time()
    while current_time - start_time < 3:
        ESOLocateCapture.get_cap()

        extras.append(
            pytest_html.extras.image(
                base_image_array(ESOLocateCapture.capture, mode='RGB')
            )
        )

        ESOLocateCapture.segmentation_test()

        extras.append(
            pytest_html.extras.image(
                base_image_array(ESOLocateCapture.capture, mode='1')
            )
        )
        current_position = ESOLocateCapture.get_current_position()
        if len(current_position) == 0:
            current_time = time.time()
        else:
            break




@pytest.fixture
def eso_locate_capture(request, extras):
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
def yet_another_compass_capture(request, extras):
    extras.append(pytest_html.extras.png(base_image_path(YET_ANOTHER_COMPASS_CAPTURE_PATH / request.param)))

    with Image.open(YET_ANOTHER_COMPASS_CAPTURE_PATH / request.param) as img:
        img.load()
    YetAnotherCompassCapture.capture = np.array(
        img.crop((YetAnotherCompassParser.left_point,
                  YetAnotherCompassParser.top_point,
                  YetAnotherCompassParser.right_point,
                  YetAnotherCompassParser.bottom_point))
    )
    extras.append(
        pytest_html.extras.image(
            base_image_array(YetAnotherCompassCapture.capture, mode='RGB')
        )
    )
    YetAnotherCompassCapture.segmentation_test(15)

@pytest.fixture(scope="session")
def mouse_sensitivity():
    # Rotation.calculate_mouse_sensitivity()
    pass