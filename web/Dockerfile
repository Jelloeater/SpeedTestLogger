# Build me from the root dir EX docker build . -f ./speed/Dockerfile
FROM python:3
ADD /web/graph-web.py /
ADD /Database /Database
RUN pip install Flask
RUN pip install pygal
RUN pip install SQLAlchemy
RUN pip install psycopg2
RUN pip install sqlalchemy-utils
RUN ls
EXPOSE 5000
ENTRYPOINT [ "python"]
CMD ["./graph-web.py"]