import logging
logging.basicConfig(format="[%(asctime)s] [%(levelname)8s] --- %(message)s "
                           "(%(filename)s:%(lineno)s)",
                    level=logging.DEBUG)
import speed_test


class TestGetSpeedTest():
    def test_doSpeedTest(self):
        logging.debug('Starting SpeedTest Unit Test')
        assert speed_test.GetSpeedTest().doSpeedTest()