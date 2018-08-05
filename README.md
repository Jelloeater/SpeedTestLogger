# SpeedTestLogger
##Buld commands
`docker-compose up -d`

**BUT**

You are going to need a Postgres DB as well, the docker-compose will provide that ^_^

To run speed test (w/ cron for example):

`docker-compose build`
`docker-compose up -d`


* Python interperter for Dockerfile.debug 
  * Alpine Image = `/usr/local/bin/python`
* See docker-compose.yml for production enviroment definition
* See individual Dockerfile's for microservice requirments
* See .gitlab-ci.yml for test enviroment

* There are two services, that BOTH use the Database class:
  * speed (for doing the actual speed tests)
  * web (for displaying the database results)
  * **If you look into the docker files you will see that the database class is nested inside the main microservice app folder**

* There are also two additional `docker-compose` files
  * `docker-compose-debug` will expose the provide a SSH'able container for remote debugging
  * `docker-compose-test` will run **pytest** unit tests for the `speed` module

##**NOTE**

You CANNOT run the docker files from the directory they are in, or you will get add errors. If you try and change it to run from where it is, you will get import errors.

It works this way, trust me.

## Credits
Borrowed SpeedTest Parser from james-atkinson/speedcomplainer