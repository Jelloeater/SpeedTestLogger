import argparse
from datetime import datetime
import email
import logging
import os

import speedtest_cli

import database

__author__ = 'jesse'


def main():
    LOG_FILENAME = 'error.log'
    parser = argparse.ArgumentParser()
    parser.add_argument("--debug",
                        action="store_true",
                        help="Debug Mode Logging")

    parser.add_argument('-g',"--getspeed",
                        action="store_true",
                        help="Test and Log Speed")

    sendspeed = parser.add_argument_group('E-mail Config')
    sendspeed.add_argument('-s', "--sendspeed",
                           action="store_true",
                           help="Send Speed Report")
    # FIXME Need to made secondary args required
    sendspeed.add_argument("-from_email")
    sendspeed.add_argument("-to_email")
    sendspeed.add_argument("-smtp_server")

    args = parser.parse_args()
    if args.debug:
        logging.basicConfig(format="[%(asctime)s] [%(levelname)8s] --- %(message)s (%(filename)s:%(lineno)s)",
                            level=logging.DEBUG)
        logging.debug('Debug Mode Enabled')
    else:
        logging.basicConfig(filename=LOG_FILENAME,
                            format="[%(asctime)s] [%(levelname)8s] --- %(message)s (%(filename)s:%(lineno)s)",
                            level=logging.WARNING)

    if args.getspeed:
        database.Setup.setup_sql_environment()
        speed_data = GetSpeedTest().doSpeedTest()
        database.SpeedTestData.put_data(speed_data)

    if args.sendspeed:
        SendSpeedTest.sendEmail(args.from_email, args.to_email, args.smtp_server, args.debug)


class SendSpeedTest():
    @staticmethod
    def getTable():
        from prettytable import PrettyTable
        x = PrettyTable()
        x.field_names = ('Timestamp', 'Upload', 'Download', 'Ping')
        data = database.SpeedTestData.get_x_days(1)
        for i in data:
            x.add_row([i.timestamp, i.up_speed, i.down_speed, i.ping])
        return x

    @staticmethod
    def sendEmail(sender, receive, SMTP_server, args_debug):
        import smtplib
        import email.utils
        from email.mime.text import MIMEText

        # Create the message
        msg = MIMEText(str(SendSpeedTest.getTable()))
        msg['To'] = email.utils.formataddr(('Recipient', receive))
        msg['From'] = email.utils.formataddr(('Author', sender))
        msg['Subject'] = 'Speed Test Report'

        server = smtplib.SMTP(SMTP_server)
        if args_debug:
            server.set_debuglevel(True) # show communication with the server
        try:
            server.sendmail(msg['From'], msg['To'], msg.as_string())
        finally:
            server.quit()


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
