# MasonJar
## API for the JamJar Application

[![Build Status](https://travis-ci.org/projectjamjar/masonjar.svg?branch=master)](https://travis-ci.org/projectjamjar/masonjar)

MasonJar handles general application requests, video uploading, audio fingerprinting, and video serving


## Setup
From the root of the `masonjar` directory (probably should be `/opt/code/masonjar`) run
```
sudo ./apt-install.sh
```
this will install all of the necessary application dependencies (python, mysql, apache, etc)

We now need to refresh our env, so run
```
source ~/.bashrc
cd /opt/code/masonjar
```

Let's install our app's python requirements
```
make install
```
*NOTE: This will probably take a while because matplotlib and scipy are huge libraries.  Be patient :)

And get the database setup
```
./database_setup.sh
make migrate
make seed
```

**WHATUPPP, you're all installed, yo!**

## Running
Since we need to run the async job queue as well as the actual server, we need two windows open, both navigated to the root directory of this repo (usually `/opt/code/masonjar/`)

In one window, run
```
make queue
```

And in another window, run
```
make run
```
This will run the server on port `5001`, so assuming you're on our VM (which has port 5001 forwarded) you should be able to access the API through `localhost:5001`


Now you should be all set!  If you're running the angular app (or testing from postman or something) you should have a default user with the following credentials:
```
Username: test
Password: password
```
