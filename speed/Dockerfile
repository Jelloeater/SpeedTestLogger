# Build me from the root dir EX docker build . -f ./speed/Dockerfile
FROM python:3.6
ADD /speed /speed
ADD /Database /speed/Database
RUN pip install -r /speed/requirements.txt
RUN echo $(ls /app -R)
#ENTRYPOINT [ "python"]
#CMD ["/speed/speed_test.py","-g", "--debug"]
