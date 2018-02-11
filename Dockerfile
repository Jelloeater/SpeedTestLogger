FROM python:3
ADD graph-web.py /
ADD test-speed.py /
ADD database.py /
RUN pip install pygal
RUN pip install speedtest-cli
RUN pip install flask
RUN pip install sqlalchemy
RUN pip install PrettyTable
EXPOSE 5000
ENTRYPOINT [ "python"]
CMD ["./graph-web.py"]