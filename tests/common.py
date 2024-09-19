import time

import numpy as np
import pytest
import pytest_html
from pathlib import Path
from pytest_check import check
from PIL import Image

from csvParser.adjacency_matrix import AdjacencyMatrixParser
from luaParser.eso_locate_parser import ESOLocateParser
from luaParser.lua_parser import LuaParser
from luaParser.yet_another_compass_parser import YetAnotherCompassParser
from matrix.destination import Destination
from moving.rotation.rotation import Rotation
from moving.gps import Gps
from moving.walking import Walking
from screenCapture.eso_locate_capture import ESOLocateCapture
from screenCapture.yet_another_compass_capture import YetAnotherCompassCapture, CardinalDirections
from common import *

CAPTURE_PATH = TEST_DIR / 'data_screen_capture'
ESO_LOCATE_CAPTURE_PATH = CAPTURE_PATH / 'locate'
YET_ANOTHER_COMPASS_CAPTURE_PATH = CAPTURE_PATH / 'compass'

