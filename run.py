from datetime import datetime
import os

__author__ = 'jesse'
class SpeedTest():
    def doSpeedTest(self):
            result = os.popen("/usr/local/bin/speedtest-cli --simple").read()
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

#TODO Query data (DONE)

#TODO Save data to SQLlite
#TODO Create DB w/ sqlalchemy

#TODO Email Report
#TODO Pretty text table module for presentation