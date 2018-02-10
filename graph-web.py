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

    date_chart = pygal.Line(x_label_rotation=-45, width=1200, height=600, explicit_size=True)

    date_chart.x_labels = [data.timestamp for data in data]

    date_chart.add("Upload", [data.up_speed/1000000 for data in data])
    date_chart.add("Download", [data.down_speed/1000000 for data in data])
    date_chart.add("Ping", [data.ping for data in data], secondary=True)
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
