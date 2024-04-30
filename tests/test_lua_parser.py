from tests.common import *


class TestLuaParser:

    def test_eso_locate_parser(self):
        ESOLocateParser.load_data()
        ESOLocateParser.set_user_property('BendreTolstyy')

        assert list(ESOLocateParser.eso_locate.keys()) == ['VictorMartyn', 'BendreTolstyy', 'WanderingWizardMikael']
        assert ESOLocateParser.left_point == -67
        assert ESOLocateParser.top_point == 67
        assert ESOLocateParser.right_point == 233
        assert ESOLocateParser.bottom_point == 87

    def test_yet_another_compass_parser(self):
        YetAnotherCompassParser.load_data()

        assert YetAnotherCompassParser.left_point == 15
        assert YetAnotherCompassParser.top_point == 89
        assert YetAnotherCompassParser.right_point == 165
        assert YetAnotherCompassParser.bottom_point == 239
