# Coding Challenge

This coding challenge required the creation of an API server for posting and
retrieving company reviews.

## Data models

All models are located at `caac/reviews/models.py`

## Installation and configuration

The configuration requires either setting environment variables or adding a
.env file with values the following variables:

- `SECRET_KEY`
- `DEBUG`
- `ALLOWED_HOSTS`
- `DATABASE_URL`

The env file should be placed inside the `cacc/cacc` directory. Also in that
directory a `sample.env` file with example values can be found.

## Installing the requirements using pipenv

`pipenv` is used to create the virtual environment and to manage the project
dependencies. It can be installed using `pip` or `pip3` depending on the system.

```
pip3 install pipenv
```

Once installed pipenv should be run from the level where the Pipfile and
Pipfile.lock are located at the project's root.


```
pipenv sync --dev
```

This creates a virtual environment and installs all dependencies

## Installing sample data

Initial fixtures can be installed by issuing the next command

```
pipenv run cacc/manage.py loaddata companies users reviews
```

All users in the sample data have their passwords set to "**password**"

## Running the server

The server can be run using the following command:

```
pipenv run caac/manage.py runserver
```

The server should be available at `127.0.0.1:8000` unless stated otherwise in
the command line


## Getting a token for interacting with the API

A JWT token is required for accessing the API. It can be obtained using by curl:

```
curl \
  -X POST \
  -H "Content-Type: application/json" \
  -d '{"username": "<username>", "password": "<password>"}' \
  http://127.0.0.1:8000/api/token/
```

Or through the url `http://127.0.0.1/api/token` using a test client.

And then adding the **access** token to the authorization header:

```
Authorization: Bearer <token>
```


## API documentation

Django Rest Framework provides automated API documentation generation when
requesting the api from browser. Swagger UI could be mounted as a documentation
alternative.
