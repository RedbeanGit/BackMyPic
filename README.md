
# Picdo

Django-based website dedicated to saving and sharing photos online.


## Installation

First clone this repo:

```bash
$ git clone git@github.com:RedbeanGit/picdo.git
```

Setup environment variables:

```bash
$ ./scripts/setup-env.sh
```

#### Install to run with Docker compose

If you plan to run Picdo inside a docker container then you just need to install [Docker compose](https://docs.docker.com/get-docker/).

#### Install to run with Python

You can also launch Picdo directly with your local Python interpreter.

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
$ ./scripts/setup-deps.sh
```

#### Note for Windows users

Scripts call Python with the `python3` command. Unfortunately on Windows the correct command is simply `python`.

One way to solve this problem is to make a copy of `python.exe` named `python3.exe` in the same folder.

The default installation folder for Python 3.8 is `C:\Users\<youUsername>\AppData\Local\Programs\Python\Python38\`.
## Run Locally

First navigate to the project root directory:

```bash
$ cd path/to/picdo
```

#### Run with Docker compose

You just need to run the following command:

```bash
$ ./scripts/run-compose.sh
```

To clean docker containers and images created by the project:

```bash
$ ./scripts/clear-docker.sh
```

#### Run with Python

If you have installed a virtual environment, activate it:

```bash
$ . env/bin/activate
```

And start the Picdo:

```bash
$ ./scripts/run-python.sh
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