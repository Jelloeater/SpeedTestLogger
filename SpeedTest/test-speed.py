import sys
sys.path.append('../')
# sys.path.append('/Database/')
import argparse
import logging
import speedtest
from prettytable import PrettyTable

# import os
# print(os.listdir(os.getcwd()))
# os.chdir('../Database')
# print(os.listdir(os.getcwd()))
from Database import databasehelper
# os.chdir('../SpeedTest')

__author__ = 'jesse'


def main():
    LOG_FILENAME = 'error.log'
    parser = argparse.ArgumentParser()
    parser.add_argument("--debug",
                        action="store_true",
                        help="Debug Mode Logging")

    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument('-g', "--getspeed",
                      action="store_true",
                      help="Test and Log Speed")

    mode.add_argument('-s', "--sendspeed",
                      action="store_true",
                      help="Send Speed Report")

    sendspeed = parser.add_argument_group('E-mail Config')
    sendspeed.add_argument("-from_email")
    sendspeed.add_argument("-to_email")
    sendspeed.add_argument("-smtp_server")

    args = parser.parse_args()
    if args.debug:
        logging.basicConfig(format="[%(asctime)s] [%(levelname)8s] --- %(message)s "
                                   "(%(filename)s:%(lineno)s)",
                            level=logging.DEBUG)
        logging.debug('Debug Mode Enabled')
    else:
        logging.basicConfig(filename=LOG_FILENAME,
                            format="[%(asctime)s] [%(levelname)8s] --- %(message)s "
                                   "(%(filename)s:%(lineno)s)",
                            level=logging.WARNING)

    if args.getspeed:
        databasehelper.Setup.setup_sql_environment()
        speed_data = GetSpeedTest().doSpeedTest()
        databasehelper.SpeedTestData.put_data(speed_data)

    if args.sendspeed:
        # SendSpeedTest.sendEmail(None,None,None,True) # DEBUG TEST
        if args.from_email and args.to_email and args.smtp_server:
            SendSpeedTest.sendEmail(args.from_email, args.to_email, args.smtp_server, args.debug)
        else:
            print('Missing all arguments')

    if args.debug:
        t = SendSpeedTest.getTable()
        logging.debug(t)


class SendSpeedTest:
    def __init__(self):
        pass

    @staticmethod
    def getTable(num_of_days=7):

        x = PrettyTable()
        x.field_names = ('Timestamp', 'Upload', 'Download', 'Ping')
        data = databasehelper.SpeedTestData.get_x_days(num_of_days)
        for i in data:
            x.add_row([str(i.timestamp).split('.')[0], i.up_speed, i.down_speed, str(int(i.ping))])
        logging.debug('\n' + str(x) + '\n')
        return x

    @staticmethod
    def getAverageData(num_of_days=7):
        data = databasehelper.SpeedTestData.get_x_days(num_of_days)
        avg = type('', (object,), {})()  # Create dummy object
        avg.up_speed = 0
        avg.down_speed = 0
        avg.ping = 0
        for i in data:
            logging.debug(i.__dict__)
            avg.up_speed = i.up_speed + avg.up_speed
            avg.down_speed = i.down_speed + avg.down_speed
            avg.ping = i.ping + avg.ping
        avg.up_speed /= len(data)
        avg.down_speed /= len(data)
        avg.ping /= len(data)
        return avg

    @staticmethod
    def sendEmail(sender, receive, SMTP_server, args_debug):
        import smtplib
        import email.utils
        from email.mime.text import MIMEText

        # Create the message
        msg = MIMEText(str(SendSpeedTest.getTable()))
        msg['To'] = email.utils.formataddr(('Recipient', receive))
        msg['From'] = email.utils.formataddr(('Author', sender))
        d = SendSpeedTest.getAverageData()
        msg['Subject'] = 'Speed Test | Avg Down: ' + str(d.down_speed) + ' | Up: ' + str(
            d.up_speed) + ' | Ping: ' + str(d.ping)

        server = smtplib.SMTP(SMTP_server)
        if args_debug:
            server.set_debuglevel(True)  # show communication with the server
        try:
            server.sendmail(msg['From'], msg['To'], msg.as_string())
        finally:
            server.quit()


class GetSpeedTest:
    def __init__(self):
        self.pingResult = None
        self.downloadResult = None
        self.uploadResult = None

    def doSpeedTest(self):
        st = speedtest.Speedtest()
        st.get_best_server()
        st.download()
        st.upload()
        self.pingResult = st.results.ping
        self.downloadResult = st.results.download
        self.uploadResult = st.results.upload
        return self


if __name__ == "__main__":
    main()
