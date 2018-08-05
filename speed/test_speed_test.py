import logging
import pytest
logging.basicConfig(format="[%(asctime)s] [%(levelname)8s] --- %(message)s "
                           "(%(filename)s:%(lineno)s)",
                    level=logging.DEBUG)
logging.debug('TEST START')
import speed_test


class TestGetSpeedTest():
    def __init__(self):
        pass

    def test_doSpeedTest(self):
        logging.debug('Starting SpeedTest Unit Test')
        assert speed_test.GetSpeedTest().doSpeedTest()