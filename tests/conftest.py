import base64
import io
from enum import Enum
from pathlib import Path
from typing import Any

from PIL import Image
from numpy import ndarray


class Requirements(Enum):
    default = 'None'
    FRS_TESO_FISHER_010101: str = ('Определить положение и размер окна ESOlocate. Данные о размере и '
                                   'положении окна ESOlocate должны быть распарщены из соответствующего файла '
                                   'и представлены в виде класса.')
    FRS_TESO_FISHER_010301: str = ('Определить положение и размер окна YetAnotherCompass. Данные о размере и '
                                   'положении окна YetAnotherCompass должны быть распарщены из соответствующего файла '
                                   'и представлены в виде класса.')


def pytest_runtest_setup(item):
    for marker in item.iter_markers(name="requirement"):
        requirement: Requirements = getattr(Requirements, marker.args[0])
        print(requirement.name + ': ' + requirement.value)


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
