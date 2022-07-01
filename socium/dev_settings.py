from .base_settings import *

# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

DEBUG = True

STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'socium',
        'USER': 'root',
        'PASSWORD': os.getenv('MYSQL_PASSWORD_DEV'),
        'OPTIONS': {'charset': 'utf8mb4'},
    }
}
