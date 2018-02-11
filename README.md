# SpeedTestLogger
Buld commands

* docker volume create speed
* docker build -t speed .

Run in order, for each component (if none specified, just run the web server):

* docker run  -d --name speed-test -v speed:/data speed "./test-speed.py" "-g" "--debug"
* docker run  -d --name speed-server -p 8080:5000 -v speed:/data speed "./graph-web.py" "--debug"

To run test:

* docker start speed-test

See Dockerfile for info

## Credits
Borrowed SpeedTest Parser from james-atkinson/speedcomplainer