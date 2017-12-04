## Install

Install django-grainy into your python env using pip

```
pip install django-grainy
```

## Django Setup

Open your django ```settings.py``` and make the following additions

#### Add to INSTALLED_APPS

```py
INSTALLED_APPS = [
    ...
    django_grainy
]
```

#### Add to AUTHETINCATION_BACKENDS

**Note**: If you have other backends you use they may give permissions to things that grainy cannot control as django only needs one of the installed backends to grant permissions for a permission check complete successfully.

The django-grainy backend extends the ```django.contrib.auth.backends.ModelBackend``` class

```py
AUTHENTICATION_BACKENDS = ["django_grainy.backends.GrainyBackend"]
```

## Run migrations

Create the django-grainy database tables

```
python manage.py migrate
```
