import argparse
import logging

__author__ = 'Jesse'
import pygal
from flask import Flask

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

    app.run()


@app.route('/')
def get_data():
    from datetime import datetime
    date_chart = pygal.Line(x_label_rotation=0, width=1200, height=600, explicit_size=True)
    date_chart.x_labels = map(lambda d: d.strftime('%Y-%m-%d'), [
        datetime(2013, 1, 2),
        datetime(2013, 1, 12),
        datetime(2013, 2, 2),
        datetime(2013, 2, 22)])
    date_chart.add("Visits", [300, 412, 823, 672])
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
    app.run()
