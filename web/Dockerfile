# Build me from the root dir EX docker build . -f ./speed/Dockerfile
FROM python:3.6
ADD /web /web
ADD /Database /web/Database
RUN pip install -r /web/requirements.txt
RUN ls
#EXPOSE 5000
ENTRYPOINT [ "python"]
CMD ["./web/graph_web.py"]