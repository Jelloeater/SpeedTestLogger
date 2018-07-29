FROM python:3
ADD . /SpeedTest
ADD . /Database
RUN pip install prettytable
RUN pip install speedtest-cli
RUN pip install SQLAlchemy
WORKDIR /SpeedTest
ENTRYPOINT [ "python"]
CMD ["./test-speed.py","-g", "--debug"]