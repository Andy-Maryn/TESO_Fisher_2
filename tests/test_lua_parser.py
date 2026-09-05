import pytest
from pytest_check import check

from luaParser.coords_and_heading_parser.coords_and_heading_parser import CoordsAndHeadingParser


class TestLuaParser:

    @pytest.mark.requirement("FRS_TESO_FISHER_010101")
    def test_coords_and_heading_parser(self, load_test_data):
        CoordsAndHeadingParser.load_data()

        check.equal(CoordsAndHeadingParser.left_point, 0)
        check.equal(CoordsAndHeadingParser.top_point, 0)
