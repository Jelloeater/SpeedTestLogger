import argparse
from datetime import datetime
import logging
import os
import speedtest_cli
import database

print(speedtest_cli.__file__)

__author__ = 'jesse'


def main():
    LOG_FILENAME = 'error.log'
    parser = argparse.ArgumentParser()
    parser.add_argument("--debug",
                        action="store_true",
                        help="Debug Mode Logging")
    args = parser.parse_args()
    if args.debug:
        logging.basicConfig(format="[%(asctime)s] [%(levelname)8s] --- %(message)s (%(filename)s:%(lineno)s)",
                            level=logging.DEBUG)
        logging.debug('Debug Mode Enabled')
    else:
        logging.basicConfig(filename=LOG_FILENAME,
                            format="[%(asctime)s] [%(levelname)8s] --- %(message)s (%(filename)s:%(lineno)s)",
                            level=logging.WARNING)

    database.Setup.setup_sql_environment()
    database.Setup.create_tables()
    data = SpeedTest().doSpeedTest()
    logging.debug(data)
    pass

    # TODO Save data to SQLlite
    # TODO Create DB w/ sqlalchemy

    # TODO Email Report
    # TODO Pretty text table module for presentation


class SpeedTest():
    def doSpeedTest(self):
        result = os.popen(str(speedtest_cli.__file__) + " --simple").read()

        if 'Cannot' in result:
            return {'date': datetime.now(), 'uploadResult': 0, 'downloadResult': 0, 'ping': 0}

        resultSet = result.split('\n')
        pingResult = resultSet[0]
        downloadResult = resultSet[1]
        uploadResult = resultSet[2]

        self.pingResult = float(pingResult.replace('Ping: ', '').replace(' ms', ''))
        self.downloadResult = float(downloadResult.replace('Download: ', '').replace(' Mbit/s', ''))
        self.uploadResult = float(uploadResult.replace('Upload: ', '').replace(' Mbit/s', ''))
        return self

if __name__ == "__main__":
    main()