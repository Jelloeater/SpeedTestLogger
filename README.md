# SpeedTestLogger
##Buld commands
`docker-compose up -d`

**BUT**

You are going to need a Postgres DB as well, the docker-compose will provide that

To run speed test (w/ cron for example):

`docker start speedtest`

* See docker-compose.yml for production
* See individual Dockerfile's for pip requirments
* See .gitlab-ci.yml for test enviroment

##**NOTE**

You CANNOT run the docker files from the directory they are in, or you will get add errors. If you try and change it to run from where it is, you will get import errors.

It works this way, trust me.

## Credits
Borrowed SpeedTest Parser from james-atkinson/speedcomplainer