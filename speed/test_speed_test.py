import logging
import os

import speed_check


class TestGetSpeedTest():
    def test_doSpeedTest(self):
        logging.info('ENVARS')
        logging.info(str(os.environ))
        assert speed_check.GetSpeedTest().doSpeedTest()


# class TestDBAccess():
#     def test_get_data_from_db(self):
#         t = speed_test.SendSpeedTest.getTable()
#         assert t is not None
