# COVID-19 Contract Explorer: Admin backend

## Getting started

Install development dependencies:

```shell
pip install pip-tools
pip-sync requirements_dev.txt
```

Set up the git pre-commit hook:

```shell
pre-commit install
```

Initialize the database:

```shell
createdb covid19_test
env DB_NAME=covid19_test ./manage.py migrate
```

Create a superuser:

```shell
env DB_NAME=covid19_test ./manage.py createsuperuser
```

Run a development server:

```shell
env DEBUG=True DB_NAME=covid19_test ./manage.py runserver
```