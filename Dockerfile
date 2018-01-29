FROM python:3
VOLUME /data
ADD run.py /
ADD database.py /
RUN pip install speedtest-cli
RUN pip install sqlalchemy
RUN pip install PrettyTable
CMD [ "python", "./run.py", "-g","--debug"]