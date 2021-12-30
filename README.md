
# Picdo

Django-based website dedicated to saving and sharing photos online.


## Installation

First install Docker compose and it's dependencies from [here](https://docs.docker.com/get-docker/).

Then clone this repo:

```bash
$ git clone git@github.com:RedbeanGit/picdo.git
```

Setup your local environment:

```bash
$ ./scripts/install.sh
```
## Run Locally

To run the project, you just need to run the following command:

```bash
$ ./scripts/run.sh
```

To clean docker containers and images created by the project:

```bash
$ ./scripts/clear-docker.sh
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