# SpeedTestLogger
Buld commands
* docker-compose up -d

OR

docker build . -f ./speed/Dockerfile

BUT

You are going to need a Postgres DB as well

To run test (w/ cron for example):

* docker start speedtest

See docker-compose.yml for production
See individual Dockerfile's for pip requirments
See .gitlab-ci.yml for test enviroment

## Credits
Borrowed SpeedTest Parser from james-atkinson/speedcomplainer