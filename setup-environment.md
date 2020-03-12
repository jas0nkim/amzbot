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

# windows 10

- install mysql 8
    https://dev.mysql.com/doc/refman/8.0/en/windows-installation.html
    (Select custom, and install ONLY MySQL Server 8.0, and select legacy password)
- install python3 and pip3
    https://docs.python.org/3/using/windows.html
- set python3 virtual environment
    python -m venv ./venv
- activate virtual env
    venv\Scripts\activate
- deactivate virtual env
    deactivate
- install python packages
    pip3 install -r requirements.txt
        install visual c++ 14 for mysqlclient package
        pip install mysqlclient-1.4.6-cp38-cp38-win32.whl
