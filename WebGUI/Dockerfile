FROM python:3
ADD . /WebGUI
ADD . /Database
RUN pip install --upgrade pip
RUN pip install Flask
RUN pip install pygal
RUN pip install SQLAlchemy
RUN pip install psycopg2
EXPOSE 5000
WORKDIR /WebGUI
ENTRYPOINT [ "python"]
CMD ["./graph-web.py"]