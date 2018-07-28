FROM python:3
ADD test-speed.py /
ADD ../Database/database.py /
RUN pip install requirements.txt
ENTRYPOINT [ "python"]
CMD ["./test-speed.py","-g", "--debug"]