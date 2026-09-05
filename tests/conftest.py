import base64
import io
import time
from pathlib import Path

import numpy as np
import psutil
import pytest
import pytest_html
from PIL import Image
from numpy import ndarray

from csvParser.adjacency_matrix import AdjacencyMatrixParser
from csvParser.requirements_parser import RequirementsParser, Requirements
from common import TEST_DIR
from luaParser.coords_and_heading_parser.coords_and_heading_parser import CoordsAndHeadingParser
from luaParser.lua_parser import LuaParser
from matrix.destination import Destination
from moving.rotation.rotation import Rotation
from screenCapture.coords_and_heading_capture.coords_and_heading_capture import CoordsAndHeadingCapture
from tests.common import COORDS_AND_HEADING_CAPTURE

processes = psutil.process_iter(['pid', 'name'])
TESO_RUNNING = True if 'eso64.exe' in [process.info['name'] for process in processes] else False

def pytest_addoption():
    RequirementsParser.load_data()


def pytest_runtest_setup(item):
    for markers in item.iter_markers(name="requirement"):
        for mark in markers.args:
            requirement= getattr(Requirements, mark)
            print(mark + ': ' + requirement)


def base_image_path(path_image: Path):
    with open(path_image, 'rb') as image_file:
        base64_bytes = base64.b64encode(image_file.read())
    return base64_bytes.decode()


def base_image_array(path_image: ndarray, mode: str):
    image = Image.new(mode, (len(path_image[0]), len(path_image)))
    pixels = image.load()

    for y in range(len(path_image)):
        for x in range(len(path_image[0])):
            if mode == '1':
                pixel = int(path_image[y][x])
            elif mode == 'RGB':
                pixel = tuple([int(i) for i in path_image[y][x]])
            else:
                pixel = 0
            pixels[x, y] = pixel

    img_byte_arr = io.BytesIO()
    image.save(img_byte_arr, format='JPEG')
    img_byte_arr = img_byte_arr.getvalue()
    base64_bytes = base64.b64encode(img_byte_arr)
    return base64_bytes.decode()

@pytest.fixture(scope="session")
def data_path():
    LuaParser._root = TEST_DIR / 'lua'
    AdjacencyMatrixParser._root = TEST_DIR / 'matrix'
    yield
    LuaParser._root = Path('C:/Users/Andrii/Documents/Elder Scrolls Online/live/SavedVariables')
    AdjacencyMatrixParser._root = TEST_DIR / 'matrix'


@pytest.fixture(scope="session")
def load_test_data(data_path):
    CoordsAndHeadingParser.load_data()
    AdjacencyMatrixParser.load_data()
    Destination.load_data()


@pytest.fixture(scope="session")
def load_data():
    CoordsAndHeadingParser.load_data()
    AdjacencyMatrixParser.load_data()
    Destination.load_data()
    yield


@pytest.fixture(scope="session")
def screen_is_ready():
    start_time = time.time()
    time.sleep(3)
    current_time = time.time()
    while current_time - start_time < 3:
        CoordsAndHeadingCapture.get_cap()

        # extras.append(
        #     pytest_html.extras.image(
        #         base_image_array(CoordsAndHeadingCapture.capture, mode='RGB')
        #     )
        # )

        CoordsAndHeadingCapture.segmentation()

        # extras.append(
        #     pytest_html.extras.image(
        #         base_image_array(CoordsAndHeadingCapture.capture, mode='1')
        #     )
        # )
        coorfs = CoordsAndHeadingCapture.get_coords()
        current_position = [coorfs.x, coorfs.y]
        if len(current_position) == 0:
            current_time = time.time()
        else:
            break


@pytest.fixture
def eso_locate_capture(request, extras):
    with Image.open(COORDS_AND_HEADING_CAPTURE / request.param) as img:
        img.load()
    CoordsAndHeadingCapture.capture = np.array(
        img.crop((CoordsAndHeadingParser.left_point,
                  CoordsAndHeadingParser.top_point,
                  CoordsAndHeadingParser.right_point,
                  CoordsAndHeadingParser.bottom_point))
    )
    extras.append(
        pytest_html.extras.image(
            base_image_array(CoordsAndHeadingCapture.capture, mode='RGB')
        )
    )
    CoordsAndHeadingCapture.segmentation(20)


@pytest.fixture(scope="session")
def mouse_sensitivity():
    Rotation.calculate_mouse_sensitivity()
    return


@pytest.fixture(scope='function', autouse=True)
def reset():
    Destination.current_destination = 0
    Destination.load_data()
