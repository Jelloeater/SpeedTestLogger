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
    data = database.SpeedTestData.get_x_days(int(last))

    date_chart = pygal.DateTimeLine(x_label_rotation=-45, width=1200, height=600, explicit_size=True,
                                    dynamic_print_values=True, value_font_size=12, human_readable=True)
    date_chart.value_formatter = lambda x: "%.2f" % x

    upload_d = []
    down_d = []
    ping_d = []
    for i in data:
        upload_d.append((i.timestamp, i.up_speed / 1000000))
        down_d.append((i.timestamp, i.down_speed / 1000000))
        ping_d.append((i.timestamp, i.ping))

    date_chart.add("Upload", upload_d)
    date_chart.add("Download", down_d)
    date_chart.add("Ping", ping_d, secondary=True)

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
