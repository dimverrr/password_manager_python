# Password Manager

Password Manager allows you to create and store your users and credentials in Docker or your own databases with API

## Installation

1. Download and install [Docker](https://www.docker.com/).

2. Download the repository on your device.

3. Create your own environment variables as it shown in .env.example file.

## Usage
1. Launch Docker

2. Run this command
```python
  docker-compose up -d --build
```
3. Then run this command
``` python
    docker-compose exec web python manage.py migrate
```

## Swagger
http://127.0.0.1:8000/swagger/
To login in Swagger click "Authorize" button and enter your token as on photo

## Postman

The postman collection file is in the repository, so you can add it to your Postman app and use it.


## Upgrade
You can upgrade the project with your own ideas using [DJANGO](https://www.djangoproject.com/):
1. Start from "password_manager" directory and views.py file.

2. Create your functions with your functionality.
All DB functions are placed in **password_manager/views.py** file, urls in **password_manager/urls.py** models in **password_manager/models.py** file.

3. Add your path and function link to urls.py file as in the repository.

### Congatulations! App is ready for use
