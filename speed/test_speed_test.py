from unittest import TestCase

import speed_test


class TestGetSpeedTest(TestCase):
    def test_doSpeedTest(self):
        assert speed_test.GetSpeedTest().doSpeedTest()
