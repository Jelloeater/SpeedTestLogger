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
    # speed_data = GetSpeedTest().doSpeedTest()
    # database.SpeedTestData.put_data(speed_data)
    SendSpeedTest.getTable()
    # TODO Email Report

class SendSpeedTest():
    @staticmethod
    def getTable():
        from prettytable import PrettyTable
        x = PrettyTable()
        x.field_names = ('Timestamp', 'Upload', 'Download', 'Ping')
        data = database.SpeedTestData.get_x_days(1)
        for i in data:
            x.add_row([i.timestamp,i.up_speed,i.down_speed,i.ping])
        return x

    @staticmethod
    def sendEmail(smtpserver):
        import smtplib
        from email import MIMEMultipart
        from email import MIMEText

        msg = MIMEMultipart()
        msg['From'] = 'me@gmail.com'
        msg['To'] = 'you@gmail.com'
        msg['Subject'] = 'simple email in python'
        message = 'here is the email'
        msg.attach(MIMEText(message))

        mailserver = smtplib.SMTP(smtpserver)
        # identify ourselves to smtp client
        mailserver.ehlo()
        mailserver.sendmail(msg['From'],msg['To'],msg.as_string())
        mailserver.quit()


class GetSpeedTest():
    def doSpeedTest(self):
        path = 'python ' + str(speedtest_cli.__file__) + " --simple"
        result = os.popen(path).read()

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