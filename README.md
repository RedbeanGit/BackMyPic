
# Picdo

Django-based website dedicated to saving and sharing photos online.


## Installation

First clone this repo:

```bash
$ git clone git@github.com:RedbeanGit/picdo.git
```

Setup your local environment:

```bash
$ ./scripts/install.sh
```

#### Install to run with Docker (recommended)

If you plan to run this project inside a docker container then you just need to
install [Docker compose](https://docs.docker.com/get-docker/).

#### Install to run with Python

You can also launch Picdo directly with a Python interpreter.

First, install [Python 3.8](https://www.python.org/downloads/).

Navigate to the project root directory:

```bash
$ cd path/to/picdo
```

Create and run a virtual environment (optional):

```bash
$ python3 -m venv env
$ . env/bin/activate
```

Setup Picdo dependencies:

```bash
$ python3 -m pip install -r requirements.txt
```

Picdo stores its data in a [Postgresql](https://www.postgresql.org/) database.
So you need to install it.

Export environment variables from `.env` file:

```bash
$ set +a
$ . .env
$ set -a
```

Then connect to Postgresql using psql.

```bash
$ psql -h PICDO_DB_HOST -p PICDO_DB_PORT
```

Create a database and a user for Picdo (replace `user`, `password` and `name` respectively by the value of `PICDO_DB_USER`, `PICDO_DB_PASSWORD` and `PICDO_DB_NAME`):

```psql
# CREATE USER user WITH PASSWORD 'password';
# CREATE DATABASE name;
```

Install the unaccent extension:

```psql
# CREATE EXTENSION IF NOT EXISTS "unaccent";
```

Finally, exit psql and let Django creating some tables:

```psql
$ python3 /src/manage.py migrate;
```
## Run Locally

First navigate to the project root directory:

```bash
$ cd path/to/picdo
```

#### Run with docker

You just need to run the following command:

```bash
$ ./scripts/run.sh
```

To clean docker containers and images created by the project:

```bash
$ ./scripts/clear-docker.sh
```

#### Run with Python

If you have installed a virtual environment, activate it:

```bash
$ source env/bin/activate
```

And start the server:

```bash
$ python3 src/manage.py runserver 0.0.0.0:8000
```
## Tech Stack

**Front-end:** HTML5, SASS, pure JS

**Back-end:** Django, Python3, Postgresql
## Environment Variables

Local environment variables are stored in `.env` file.

**`PICDO_VERSION`**

The current version of Picdo.

**`PICDO_SECRET_KEY`**

A string used by Django to encode sensitive data. Default is auto-generated.

**`PICDO_ENVIRONMENT`**

The current environment. Should be `DEVELOPMENT`, `STAGING` or `PRODUCTION`. Default is `DEVELOPMENT`.

**`PICDO_DB_NAME`**

The name of the database to store data. Default is `picdo`.

**`PICDO_DB_HOST`**

The hostname or address of the database to connect. Default is `db`.

**`PICDO_DB_PORT`**

The port to use to connect to the database. Default is `5432`.

**`PICDO_DB_USER`**

The user of the database. Default is `postgres`.

**`PICDO_DB_PASSWORD`**

The password used to authenticate to the database. Default is auto-generated.