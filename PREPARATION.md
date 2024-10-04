# Prior-Deployment 

## Setting Up
    python -m venv .venv
    venv/Scripts/activate

    pip3 install Django
    django-admin startproject Project-Name
    cd Project-Name

## .env File

    pip install django-environ

here is the sample of .env file:

    ADMIN_URL='admin/'
    SECRET_KEY=SECRET
    ALLOWED_HOSTS=['*']
    CSRF_TRUSTED_ORIGINS=["http://127.0.0.1:8000]

    DB_ENGINE_NAME=mysql
    DB_NAME='dbname'
    DB_USER='user'
    DB_PASSWORD=password
    DB_HOST='localhost'
    DB_PORT=3306

In settings.py:

    from pathlib import Path
    import environ
    import os

    BASE_DIR = Path(__file__).resolve().parent.parent.parent

    env = environ.Env()
    environ.Env.read_env(os.path.join(BASE_DIR, '.env'))

    SECRET_KEY = env('SECRET_KEY')

## MySQL database

    python manage.py dumpdata --output=data.json
    pip install mysqlclient

### Add to Settings

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': os.getenv('DB_NAME'),
            'USER': os.getenv('DB_USER'),
            'PASSWORD': os.getenv('DB_PASSWORD'),
            'HOST': os.getenv('DB_HOST'), #localhost
            'PORT': os.getenv('DB_PORT'), #3306
        }
    }

migrate data:

    python manage.py makemigrations
    python manage.py migrate 
    python manage.py loaddata data.json

## Requirements

Create a new folder `requirements`

    pip3 freeze > requirements/dev.txt
    pip3 freeze > requirements/prod.txt

## Settings

Create a folder 'settings' within the project
create ```__init__.py```
create ```base.py``` and copy-paste from initial settings.
in the ```base.py``` add ```.parent```
delete settings.py

create ```dev.py``` and add database sqllite for development purposes
create ```prod.py``` and add MySQL for production

Example `settings/dev.py`:

    from .base import *

    DEBUG = True
    ALLOWED_HOSTS = ['*']

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

Example `settings/prod.py`:

    from .base import *

    DEBUG = False
    ALLOWED_HOSTS = list(env('ALLOWED_HOSTS'))
    CSRF_TRUSTED_ORIGINS = list(env('CSRF_TRUSTED_ORIGINS'))

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': env('DB_NAME'),
            'USER': env('DB_USER'),
            'PASSWORD': env('DB_PASSWORD'),
            'HOST': env('DB_HOST'),
            'PORT': env('DB_PORT'),
        }
    }


## Separating Frontend

    TEMPLATES = [
        {
            'BACKEND': 'django.template.backends.django.DjangoTemplates',
            'DIRS': [os.path.join(BASE_DIR, 'frontend/templates/')],
            ...           
        },
    ]

    STATIC_URL = '/static/'
    STATICFILES_DIRS = [
        os.path.join(BASE_DIR, 'frontend/static/'),
    ]
    STATIC_ROOT = os.path.join(BASE_DIR, 'static')

## Adding Images and Media

    pip install pillow

```settings.py```:
    
    MEDIA_URL = '/media/'
    MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

```urls.py```:

    from django.contrib import admin
    from django.urls import path, include
    from django.conf import settings
    from django.conf.urls.static import static

    urlpatterns = [
        path('admin/', admin.site.urls),
        path('', include('app-name.urls'))
    ]

    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


## WSGI

In the ``wsqi.py`` add ``prod`` to the end:


    from django.core.wsgi import get_wsgi_application

    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'your-project-name.settings.prod')

    application = get_wsgi_application()

### Using Waitress:

    pip install waitress

### Or using Gunicorn:

    pip install gunicorn

## Running App

Running locally:

    python manage.py runserver --settings=deployment.settings.dev

Running via Waitress:

    waitress-serve --listen=*:8000 deployment.wsgi:application

    waitress-serve --listen=127.0.0.1:8000 deployment.wsgi:application

Or run with Gunicorn

    gunicorn deployment.wsgi -b 127.0.0.1:8000
