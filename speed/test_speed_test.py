import logging
logging.basicConfig(format="[%(asctime)s] [%(levelname)8s] --- %(message)s "
                           "(%(filename)s:%(lineno)s)",
                    level=logging.DEBUG)
from unittest import TestCase
import speed_test


class TestGetSpeedTest(TestCase):
    def test_doSpeedTest(self):
        logging.debug('Starting SpeedTest Unit Test')
        assert speed_test.GetSpeedTest().doSpeedTest()

TestGetSpeedTest().test_doSpeedTest()