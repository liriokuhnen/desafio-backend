TBE
==============

"Travel Book Evaluate" is a booking notes about your travels

# Dependencies

The dependencies to running this project is Docker, Docker Compose and Python 3.7 although is possible running without docker using virtualenv

# Run with Docker:

Docker is awesome! to configure your local container and create initial data on your database run this commands

```
docker-compose build
docker-compose run web python3 manage.py loaddata api/fixtures/initial.json
```

to run

```
docker-compose up
```

you can check the site on http://127.0.0.1:8000/admin and can login with username admin and password 123123 (you can use that user to create a Auth Token)

# Run tests on Docker:

Just use this command

```
docker-compose run web python3 manage.py test
```

# Run with Virtualenv:

You will need virtualenv so if you don´t have installed [click here](https://virtualenv.pypa.io/en/latest/installation.html)

Create your env and activate

```
virtualenv -p python3 env
source env/bin/activate
```

Install python libs requirements

```
pip3 install -r requirements/requirements_local.txt
```

Make migrations to database

```
python3 manage.py migrate
```

create initial data on your database, that will create a super user with username admin and password 123123 (you can use that user to create a Auth Token)

```
python3 manage.py loaddata api/fixtures/initial.json
```

before run application it is important to know that the project have specific configurations for environment (prod, stage, local and docker) to choose one just create ENV like a environment variable (to run local is not necessary)

```
export ENV=local
```

to run application

```
python3 manage.py runserver
```

# Run tests:

to run tests you have to be with your env activated

```
python3 manage.py test
```

# REST API
If you use postman you can import the library with requests at file "desafio-tembici.postman_collection.json"

The REST API to the example app is described below.

## Auth Token

### Request

`POST /api/v1/token/`

### Headers
    Content-Type: application/json

### Body Json

    {
    	"username": "admin",
    	"password": "123123"
    }

### Curl Example
    curl --location --request POST 'http://127.0.0.1:8000/api/v1/token/' \
    --header 'Content-Type: application/json' \
    --data-raw '{
    	"username": "admin",
    	"password": "123123"
    }'

### Response

    {
        "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTU4OTYwODc1MSwianRpIjoiZjc5YjVmZjMzOTgyNDM2YWJjYWMzOGQyYTg3MmFhODIiLCJ1c2VyX2lkIjoxfQ.V-8ic6oQ2oVzExUrzkiSLDQ6nDN-Rlx44G5mvheR1ic",
        "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNTg5OTU0MzUxLCJqdGkiOiI1NjM1MjkyYmQzNGY0MmU2ODQzN2ZkOGVjMGNmZDFjYyIsInVzZXJfaWQiOjF9.eKYv5cb3fVwdVb4I9J5MTFunbnEgQidefVBlnuux_W8"
    }

## Get Travels

### Request

`GET /api/v1/travel/`

### Headers

    Authorization: Bearer <Access Token>
    Content-Type: application/json

### Curl Example
    curl --location --request GET 'http://127.0.0.1:8000/api/v1/travel/' \
    --header 'Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNTg5OTU0MzUxLCJqdGkiOiI1NjM1MjkyYmQzNGY0MmU2ODQzN2ZkOGVjMGNmZDFjYyIsInVzZXJfaWQiOjF9.eKYv5cb3fVwdVb4I9J5MTFunbnEgQidefVBlnuux_W8'

### Response

    {
        "count": 3,
        "next": "http://127.0.0.1:8000/api/v1/travel/?limit=2&offset=2",
        "previous": null,
        "results": [
            {
                "id": 3,
                "start_date": "2020-05-10T23:50:02Z",
                "finish_date": "2020-05-10T23:50:02Z",
                "classification": null,
                "evaluate": 1
            },
            {
                "id": 2,
                "start_date": "2020-05-10T23:50:02Z",
                "finish_date": "2020-05-10T23:50:02Z",
                "classification": null,
                "evaluate": null
            }
        ]
    }

## Update Travel

### Request

`PATCH /api/v1/travel/<travel_id>/`

### Headers

    Authorization: Bearer <Access Token>
    Content-Type: application/json

### Body Json

    {
        "classification": 2,
        "evaluate": 1
    }

### Curl Example
    curl --location --request PATCH 'http://127.0.0.1:8000/api/v1/travel/3/' \
    --header 'Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNTg5OTU0MzUxLCJqdGkiOiI1NjM1MjkyYmQzNGY0MmU2ODQzN2ZkOGVjMGNmZDFjYyIsInVzZXJfaWQiOjF9.eKYv5cb3fVwdVb4I9J5MTFunbnEgQidefVBlnuux_W8' \
    --header 'Content-Type: application/json' \
    --data-raw '{
        "classification": 2,
        "evaluate": 1
    }'

### Response

    {
        "id": 3,
        "start_date": "2020-05-10T23:50:02Z",
        "finish_date": "2020-05-10T23:50:02Z",
        "classification": 2,
        "evaluate": 1
    }

## Create Travel

### Request

`POST /api/v1/travel/`

### Headers

    Authorization: Bearer <Access Token>
    Content-Type: application/json

### Body Json

    {
        "start_date": "2020-05-01T06:02:18Z",
        "finish_date": "2029-05-05T06:02:18Z"
    }

### Curl Example
    curl --location --request POST 'http://127.0.0.1:8000/api/v1/travel/' \
    --header 'Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNTg5OTU0MzUxLCJqdGkiOiI1NjM1MjkyYmQzNGY0MmU2ODQzN2ZkOGVjMGNmZDFjYyIsInVzZXJfaWQiOjF9.eKYv5cb3fVwdVb4I9J5MTFunbnEgQidefVBlnuux_W8' \
    --header 'Content-Type: application/json' \
    --data-raw '{
        "start_date": "2020-05-01T06:02:18Z",
        "finish_date": "2029-05-05T06:02:18Z"
    }'

### Response

    {
        "id": 7,
        "user": 1,
        "start_date": "2020-05-01T06:02:18Z",
        "finish_date": "2029-05-05T06:02:18Z",
        "classification": null,
        "evaluate": null
    }


# Related Documentation

[Django](https://docs.djangoproject.com/en/3.0/)

[Django Rest Framework](https://www.django-rest-framework.org/)

[Django Rest Framework SimpleJwt](https://django-rest-framework-simplejwt.readthedocs.io/en/latest/index.html)