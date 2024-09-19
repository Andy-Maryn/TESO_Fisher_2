import base64
import io

import psutil
from numpy import ndarray

from csvParser.requirements_parser import RequirementsParser, Requirements
from tests.common import *

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
    yield


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

        ESOLocateCapture.segmentation()

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
    ESOLocateCapture.segmentation(20)


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
    YetAnotherCompassCapture.segmentation(13)


@pytest.fixture(scope="session")
def mouse_sensitivity():
    Rotation.calculate_mouse_sensitivity()
    return


@pytest.fixture(scope='function', autouse=True)
def reset():
    Destination.current_destination = 0
    Destination.load_data()
