# DECOR
A simple API built with Django, Docker, Postgres and more...
Inspired by Pinterest

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.


# USAGE

```
$ git clone https://github.com/FremahA/DECOR

# Create a .env file from the .env.example file provided and fill in the necessary details.
# Create a folder called `logs`. All API logs will be stored in this folder

$ cd decor

$ docker-compose build
$ docker-compose up
```

## Access container and create super user 
```
$ docker ps

$docker exec -it CONTAINER ID /bin/bash

$ python manage.py createsuperuser --email admin@example.com --username admin"
First Name: admin
Last Name: admin
Password: password123
Password (again): password123
Bypass password validation and create user anyway? [y/N]: y
Superuser created successfully.
```

## Start server

```
$ docker-compose up
```

Start server in detached mode:

```
$ docker-compose up -d
```

## API location

* Go to `http://localhost:8000` to browse public RESTful APIs
* Django Admin: `http://localhost:8000/admin`
* Log in with admin user:
+ Username: admin
+ Password: `<the password you filled in at the step creating admin user>`

## References

+ [https://docs.docker.com/compose/django/](https://docs.docker.com/compose/django/)
+ [https://www.django-rest-framework.org/tutorial/quickstart/](https://www.django-rest-framework.org/tutorial/quickstart/)

