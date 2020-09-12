# TEDxRUPP Ticket scanning system (BACKEND)

This is a scanning system used for scanning ticket for the audiences

## Setup

### Setup database
> download mysql

```
mysql -u root -p
```

Then type your password then

```
create database ticket;
```

> change password in file configuration.py SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:**yourpassword**@localhost/ticket"

### Setup server

**Windows**
```
pip install --user virtualenv

python3 -m venv env

.\env\Scripts\activate

pip3 install -r requirements.txt

python3 run.py
```

**Macos/Linux**
```
pip install --user virtualenv

python3 -m venv env

source env/bin/activate

pip3 install -r requirements.txt

python3 run.py
```

### Test the API

{{PROTOCOL}}://{{HOST}}:{{PORT}}

**Routes**
/codes
/login
/scan
/upload
/audiences
