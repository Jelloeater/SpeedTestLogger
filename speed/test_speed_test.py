import logging
import os

import speed_test


class TestGetSpeedTest():
    def test_doSpeedTest(self):
        logging.info('ENVARS')
        logging.info(str(os.environ))
        assert speed_test.GetSpeedTest().doSpeedTest()


# class TestDBAccess():
#     def test_get_data_from_db(self):
#         t = speed_test.SendSpeedTest.getTable()
#         assert t is not None
