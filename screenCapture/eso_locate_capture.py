import numpy as np
import pytesseract
from PIL import Image, ImageFilter

from luaParser.eso_locate_parser import ESOLocateParser
from screenCapture.screen_capture import ScreeCapture


class ESOLocateCapture(ScreeCapture):
    main_color = np.array([207, 220, 189])

    img: Image

    @classmethod
    def get_cap(cls, **kwargs):
        super().get_cap(
            point_left=ESOLocateParser.left_point,
            point_top=ESOLocateParser.top_point,
            point_right=ESOLocateParser.right_point,
            point_bottom=ESOLocateParser.bottom_point)

        cls.capture = cls.capture[:, 100:200, :]

    @classmethod
    def convert_image_2_text(cls):
        cls.img = cls.resize_xn(
            Image.fromarray(
                obj=cls.capture,
                mode='RGB'
            ), [3, 3]
        )

        for _ in range(1):
            cls.img = cls.img.filter(ImageFilter.MinFilter(3))
        return pytesseract.image_to_string(cls.img, config='r-l equ')
