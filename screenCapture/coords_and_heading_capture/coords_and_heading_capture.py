"""ESOLocate capture"""
import json
import re
from dataclasses import dataclass
from typing import NamedTuple

import cv2
import pytesseract

from luaParser.coords_and_heading_parser.coords_and_heading_parser import CoordsAndHeadingParser
from screenCapture.screen_capture import *


# PATTERN = r"\d{2,3}[.,]\d{2}.*?\d{2,3}[.,]\d{2}\n"

@dataclass(frozen=True)
class CoordsAndHeading:
    x: int
    y: int
    z: int
    zone_id: int
    char_heading: int
    camera_heading: int

class Coords(NamedTuple):
    x: int
    y: int
    z: int


class Heading(NamedTuple):
    char_heading: int
    camera_heading: int


class CoordsAndHeadingCapture(ScreeCapture):
    """Captures an image of CoordsAndHeading coordinates"""
    # main_color = np.array([207, 220, 189])
    main_color = np.array([0, 0, 0])

    _digit_size = 8
    _sign_size = 4
    _space_size = 8
    # convert_format: str = '00.00 00.00'
    # convert_format_digit = []
    # with open(ROOT / r"screenCapture\coords_and_heading_capture\eso_locate_masks.json", mode="r",
    #           encoding="utf-8") as file:
    #     _digits: dict[str, int] = json.load(file)
    #
    # __val = 0
    # for i in convert_format:
    #     if i.isdigit():
    #         __val += _digit_size
    #         convert_format_digit.append(__val)
    #     elif i.isspace():
    #         __val += _space_size
    #         convert_format_digit.append(__val)
    #     else:
    #         __val += _sign_size
    #         convert_format_digit.append(__val)

    # ------------------------------------------------------------------
    # OCR configuration
    # ------------------------------------------------------------------

    # Characters which can occur in the numeric values.
    _ocr_config = "--psm 6 "

    # A number can be:
    #   123
    #   -123
    #   +123
    #   123.45
    #   -123.45
    #   123,45
    _number_pattern = re.compile(
        r"[-+]?\d+(?:[.,]\d+)?"
    )

    _NUMERIC_LINES = {
        0,  # X
        1,  # Y
        2,  # Z
        3,  # ZoneId
        6,  # CharHeading
        7,  # CameraHeading
    }

    _OCR_DIGIT_REPLACEMENTS = str.maketrans({
        "O": "0",
        "o": "0",
        "Q": "0",

        "I": "1",
        "l": "1",
        "i": "1",
        "|": "1",

        "Z": "2",
        "z": "2",

        "S": "5",
        "s": "5",

        "G": "6",
        "b": "6",

        "T": "7",

        "B": "8",

        "g": "9",
    })

    # ------------------------------------------------------------------
    # Capture
    # ------------------------------------------------------------------

    @classmethod
    def get_cap(cls, **kwargs) -> ndarray[Any, dtype[Any]]:
        """Capture the coordinates/heading area."""
        super().get_cap(point_left=CoordsAndHeadingParser.left_point, point_top=CoordsAndHeadingParser.top_point,
            point_right=CoordsAndHeadingParser.right_point, point_bottom=CoordsAndHeadingParser.bottom_point)

        # cls.capture = cls.capture[5:18, 110:190]
        return cls.capture

    # ------------------------------------------------------------------
    # Image preprocessing
    # ------------------------------------------------------------------

    @classmethod
    def _prepare_for_ocr(cls, image: ndarray) -> ndarray:
        if image is None or image.size == 0:
            raise AssertionError("Coordinates capture is empty.")

        # BGR -> grayscale
        if image.ndim == 3:
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        else:
            gray = image.copy()

        # float64 -> uint8
        if gray.dtype != np.uint8:
            min_value = np.min(gray)
            max_value = np.max(gray)

            if max_value > min_value:
                gray = (
                        (gray - min_value)
                        / (max_value - min_value)
                        * 255
                ).astype(np.uint8)
            else:
                gray = np.zeros_like(
                    gray,
                    dtype=np.uint8,
                )

        # Enlarge text
        gray = cv2.resize(
            gray,
            None,
            fx=4,
            fy=4,
            interpolation=cv2.INTER_CUBIC,
        )

        # Convert to white text on black background.
        _, binary = cv2.threshold(
            gray,
            0,
            255,
            cv2.THRESH_BINARY + cv2.THRESH_OTSU,
        )

        return binary

    # ------------------------------------------------------------------
    # OCR
    # ------------------------------------------------------------------

    @classmethod
    def get_text(cls) -> str:
        """
        Perform OCR on the captured coordinates/heading area.
        """

        image = cls._prepare_for_ocr(cls.capture)

        return pytesseract.image_to_string(
            image,
            config=cls._ocr_config,
        )

    @classmethod
    def get_numbers(cls) -> CoordsAndHeading:
        """
        Extract expected numeric fields in their known order.

        String fields are ignored completely.
        OCR errors in numeric fields are corrected when possible.
        """

        text = cls.get_text()

        lines = [
            line.strip()
            for line in text.splitlines()
            if line.strip()
        ]

        result = []

        for index in cls._NUMERIC_LINES:

            if index >= len(lines):
                raise AssertionError(
                    f"Expected numeric line {index}, "
                    f"but OCR returned only {len(lines)} lines.\n\n"
                    f"OCR text:\n{text}"
                )

            line = lines[index]

            if ":" not in line:
                raise AssertionError(
                    f"Expected ':' in numeric line {index}:\n"
                    f"{line!r}\n\n"
                    f"OCR text:\n{text}"
                )

            value = line.split(":", 1)[1].strip()

            number = cls._parse_numeric_value(value)

            # if number is None:
            #     raise AssertionError(
            #         f"Could not parse numeric value from line "
            #         f"{index}:\n"
            #         f"{line!r}\n\n"
            #         f"OCR text:\n{text}"
            #     )

            result.append(number)

        return CoordsAndHeading(*result)

    @classmethod
    def get_coords(cls) -> Coords:
        data = cls.get_numbers()
        return Coords(
            data.x,
            data.y,
            data.z,
        )

    @classmethod
    def get_heading(cls) -> Heading:
        data = cls.get_numbers()
        return Heading(
            data.char_heading,
            data.camera_heading,
        )


    @classmethod
    def _parse_numeric_value(cls, value: str) -> int | float | None:
        """
        Try to recover a numeric value from OCR output.

        Returns None if the value cannot reasonably be interpreted
        as a number.
        """

        value = value.strip()

        # Remove degree sign
        value = value.rstrip("°").strip()

        # OCR → digit corrections
        value = value.translate(
            cls._OCR_DIGIT_REPLACEMENTS
        )

        # Keep only characters which can participate in a number.
        value = re.sub(
            r"[^0-9+\-.,]",
            "",
            value,
        )

        if not value:
            return None

        # Find number
        match = re.fullmatch(
            r"[-+]?\d+(?:[.,]\d+)?",
            value,
        )

        if match is None:
            return None

        value = value.replace(",", ".")

        if "." in value:
            return float(value)

        return int(value)
