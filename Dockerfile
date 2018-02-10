FROM python:3
VOLUME /data
ADD run.py /
ADD database.py /
RUN pip install pygal
RUN pip install flask
RUN pip install sqlalchemy
CMD [ "python", "./run.py", "-g","--debug"]