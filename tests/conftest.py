import base64
import io
from pathlib import Path

import psutil
from PIL import Image
from numpy import ndarray

from tools.csv_parser.requirements_parser import Requirements, RequirementsParser

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
