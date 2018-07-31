# Build me from the root dir EX docker build . -f ./speed/Dockerfile
FROM python:3
ADD /web /
ADD /Database /Database
RUN pip install -r requirements.txt
RUN ls
EXPOSE 5000
ENTRYPOINT [ "python"]
CMD ["./graph_web.py"]