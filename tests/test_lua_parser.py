from tests.common import *


class TestLuaParser:

    @pytest.mark.requirement("FRS_TESO_FISHER_010101")
    def test_eso_locate_parser(self, load_test_data):
        ESOLocateParser.load_data()
        ESOLocateParser.set_user_property('BendreTolstyy')

        check.equal(list(ESOLocateParser.eso_locate.keys()), ['BendreTolstyy'])
        check.equal(ESOLocateParser.left_point, 5)
        check.equal(ESOLocateParser.top_point, 0)
        check.equal(ESOLocateParser.right_point, 305)
        check.equal(ESOLocateParser.bottom_point, 20)

    def test_yet_another_compass_parser(self, load_test_data):
        YetAnotherCompassParser.load_data()

        check.equal(YetAnotherCompassParser.left_point, 238)
        check.equal(YetAnotherCompassParser.top_point, 90)
        check.equal(YetAnotherCompassParser.right_point, 388)
        check.equal(YetAnotherCompassParser.bottom_point, 240)
