# Build me from the root dir EX docker build . -f ./speed/Dockerfile
FROM python:3
ADD /speed /
ADD /Database /Database
RUN pip install prettytable
RUN pip install speedtest-cli
RUN pip install SQLAlchemy
RUN pip install psycopg2
RUN pip install sqlalchemy-utils
RUN pip install pytest
RUN ls
ENTRYPOINT [ "python"]
CMD ["./speed_test.py","-g", "--debug"]