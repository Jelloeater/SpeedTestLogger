FROM python:3
ADD . /SpeedTest
ADD . /Database
#RUN pip install --upgrade pip
#RUN pip install prettytable
#RUN pip install speedtest-cli
#RUN pip install SQLAlchemy
#RUN pip install psycopg2
WORKDIR /SpeedTest
ENTRYPOINT [ "python"]
CMD ["./test-speed.py","-g", "--debug"]