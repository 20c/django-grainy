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
        MIDDLEWARE = [
            'django.middleware.security.SecurityMiddleware',
            'django.contrib.sessions.middleware.SessionMiddleware',
            'django.middleware.common.CommonMiddleware',
            'django.middleware.csrf.CsrfViewMiddleware',
            'django.contrib.auth.middleware.AuthenticationMiddleware',
            'django.contrib.messages.middleware.MessageMiddleware',
            'django.middleware.clickjacking.XFrameOptionsMiddleware',
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
