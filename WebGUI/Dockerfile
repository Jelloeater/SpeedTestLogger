FROM python:3
ADD graph-web.py /
ADD ../Database/database.py /
RUN pip install requirements.txt
EXPOSE 5000
ENTRYPOINT [ "python"]
CMD ["./graph-web.py"]