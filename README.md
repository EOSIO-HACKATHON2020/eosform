# EOSFORM
---

## Requirements

- Python 3.8
- Django 3.0+
- PostgreSQL 11+

## Install

```bash
# create virtual environment
python3.8 -m venv .venv
source .venv/bin/activate
# put env variables
touch .env
pip install -r requirements.txt
createdb eosform
export DATABASE_URL=postgres://localhost/eosform
python manage.py migrate
```

## Run

```bash
make
```
