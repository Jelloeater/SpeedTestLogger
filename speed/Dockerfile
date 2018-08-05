# Build me from the root dir EX docker build . -f ./speed/Dockerfile
FROM python:3.6
ADD /speed /
ADD /Database /Database
RUN pip install -r requirements.txt
RUN ls
ENTRYPOINT [ "python"]
CMD ["./speed_test.py","-g", "--debug"]