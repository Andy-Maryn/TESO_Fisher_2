import pytest

from tests.common import *


class TestLuaParser:

    @pytest.mark.requirement("FRS_TESO_FISHER_010101")
    def test_eso_locate_parser(self, load_test_data):
        ESOLocateParser.load_data()
        ESOLocateParser.set_user_property('BendreTolstyy')

        assert list(ESOLocateParser.eso_locate.keys()) == ['BendreTolstyy']
        assert ESOLocateParser.left_point == 5
        assert ESOLocateParser.top_point == 0
        assert ESOLocateParser.right_point == 305
        assert ESOLocateParser.bottom_point == 20

    @pytest.mark.requirement("FRS_TESO_FISHER_010301")
    def test_yet_another_compass_parser(self, load_test_data):
        YetAnotherCompassParser.load_data()

        assert YetAnotherCompassParser.left_point == 238
        assert YetAnotherCompassParser.top_point == 90
        assert YetAnotherCompassParser.right_point == 388
        assert YetAnotherCompassParser.bottom_point == 240
