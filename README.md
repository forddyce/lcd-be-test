# lcd-be-test

Guide for ubuntu machine:

- make sure python3 and mysql server is installed in your machine
- install sqlalchemy connector to mysql
  `apt install libmysqlclient-dev -y` (i'm not sure this is needed anymore since i realized python 3.12 doesnt use this)

- install venv python
  `apt install python3-pip python3-venv -y`

- create virtual env
  `cd appFolder && python3 -m venv venv`

- run the venv
  `source venv/bin/activate`

- inside the active virtual env, run
  `pip install -r requirements.txt`

- copy and rename the `env.sample` to `env`, change the `env` info to the setup of your machine

- run the app:
  `python main.py` <-- this is the root main.py, _not_ the one inside app folder

if you go to http://127.0.0.1:8000/, you should see the success message, means setup is OK.

[update]
added postman collection on root for testing
