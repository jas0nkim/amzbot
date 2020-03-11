# macos

- install mysql 8 via homebrew:
    brew install mysql@8.0
- run mysql server:
    brew services start mysql
- check mysql server started:
    brew services
- setup mysql root user password:
    mysql_secure_installation
- install python3 and pip3
    brew install python3
    brew install pip3
- set python3 virtual environment
    python3 -m venv ./venv
- activate virtual env
    source ./venv/bin/activate
- deactivate virtual env
    deactivate
- install python packages
    pip3 install -r ./requirements.txt

