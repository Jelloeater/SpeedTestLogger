import argparse
import logging

import pygal
from flask import Flask

import database

__author__ = 'Jesse'

app = Flask(__name__)


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

    if args.debug:
        logging.debug('DEBUG MODE ON`')


@app.route('/')
def get_data():
    return get_data_last(7)


@app.route('/<last>')
def get_data_last(last):
    data = database.SpeedTestData.get_x_days(last)

    date_chart = pygal.DateTimeLine(x_label_rotation=-45, width=1200, height=600, explicit_size=True,
                                    # x_value_formatter=lambda dt: dt.strftime('%d, %b %Y at %I:%M:%S %p')
                                    )

    # date_chart.x_labels = [data.timestamp for data in data]


    # date_chart = pygal.DateTimeLine(
    #     x_label_rotation=35, truncate_label=-1,
    #     x_value_formatter=lambda dt: dt.strftime('%d, %b %Y at %I:%M:%S %p'))
    # date_chart.add("Serie", [
    #     (datetime(2013, 1, 2, 12, 0), 300),
    #     (datetime(2013, 1, 12, 14, 30, 45), 412),
    #     (datetime(2013, 2, 2, 6), 823),
    #     (datetime(2013, 2, 22, 9, 45), 672)
    # ])
    # date_chart.render()
    #





    time_d = [data.timestamp for data in data]
    upload_d = [data.up_speed / 1000000 for data in data]
    down_d = [data.down_speed / 1000000 for data in data]
    ping_d = [data.ping for data in data]

    up_time_d = time_d,upload_d
    #
    # date_chart.add("Upload", [time_d,upload_d])
    # date_chart.add("Download", [time_d,down_d])
    # date_chart.add("Ping", [time_d,ping_d], secondary=True)
    # date_chart.add("Upload", [time_d,upload_d])

    # date_chart.add("Upload", up_time_d)



    data1= [time_d[0], upload_d[0]]
    data2= [time_d[1], upload_d[1]]
    data3= [time_d[2], upload_d[2]]
    data_list= data1,data2,data3
    date_chart.add("Upload2", data_list)















    date_chart.render()

    html = """
        <html>
              <body>
                 {}
             </body>
        </html>
        """
    html = html.format(date_chart.render())

    return html


# ----------------------------------------------------------------------
if __name__ == '__main__':
    main()
    # x=get_data()
    app.run()
