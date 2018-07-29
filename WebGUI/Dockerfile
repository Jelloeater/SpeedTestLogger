FROM python:3
ADD . /WebGUI
ADD . /Database
RUN pip install Flask
RUN pip install pygal
RUN pip install SQLAlchemy
EXPOSE 5000
WORKDIR /WebGUI
ENTRYPOINT [ "python"]
CMD ["./graph-web.py"]