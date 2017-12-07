from django.conf import settings

def pytest_configure():
    settings.configure(
        SECRET_KEY="sekret",
        ROOT_URLCONF="django_grainy_test.urls",
        INSTALLED_APPS=[
            'django.contrib.auth',
            'django.contrib.contenttypes',
            'django.contrib.admin',
            'django.contrib.sessions',
            'django_grainy',
            'django_grainy_test'
        ],
        DATABASE_ENGINE='django.db.backends.sqlite3',
        DATABASES={
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': ':memory:',
            }
        },
        GRAINY_ANONYMOUS_PERMS={
            "a.b.c" : 0x01,
            "a.b.c.d" : 0x01 | 0x02
        },
        DEBUG=True
    )
