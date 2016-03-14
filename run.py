from datetime import datetime
import os

__author__ = 'jesse'

def detectOS():
    from sys import platform as _platform
    if _platform == "linux" or _platform == "linux2":
        pass
    # linux
    elif _platform == "darwin":
        pass
    # MAC OS X
    elif _platform == "win32":
        pass
    # Windows

class SpeedTest():
    def doSpeedTest(self):
            result = os.popen("/usr/local/bin/speedtest-cli --simple").read()
            # TODO Add switch for different OS versions

            if 'Cannot' in result:
                return { 'date': datetime.now(), 'uploadResult': 0, 'downloadResult': 0, 'ping': 0 }

            resultSet = result.split('\n')
            pingResult = resultSet[0]
            downloadResult = resultSet[1]
            uploadResult = resultSet[2]

            self.pingResult = float(pingResult.replace('Ping: ', '').replace(' ms', ''))
            self.downloadResult = float(downloadResult.replace('Download: ', '').replace(' Mbit/s', ''))
            self.uploadResult = float(uploadResult.replace('Upload: ', '').replace(' Mbit/s', ''))
            return self

data=SpeedTest().doSpeedTest()

#TODO Save data to SQLlite
#TODO Create DB w/ sqlalchemy

#TODO Email Report
#TODO Pretty text table module for presentation