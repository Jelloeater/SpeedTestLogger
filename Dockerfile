FROM python:3
VOLUME /data
ADD graph-web.py /
ADD test-speed.py /
ADD database.py /
RUN pip install pygal
RUN pip install speedtest-cli
RUN pip install flask
RUN pip install sqlalchemy
RUN pip install PrettyTable

# For Running Web server
CMD [ "python", "./graph-web.py", "--debug"]

# For testing speed
#CMD [ "python", "./test-speed.py", "-g","--debug"]