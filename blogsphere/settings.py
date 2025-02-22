
import os
from pathlib import Path
from decouple import config
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET_KEY')
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config('DEBUG')

ALLOWED_HOSTS = ['*']
# ALLOWED_HOSTS = ['localhost', '127.0.0.1', 'testserver']
SITE_ID = 3

# AUTHENTICATION_BACKENDS = [
#     'users.backends.EmailBackend',  # Add this
#     'django.contrib.auth.backends.ModelBackend',  # Default
#     'allauth.account.auth_backends.AuthenticationBackend',  # django-allauth backend
# ]
# Application definition

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',  # Default Django authentication
    'allauth.account.auth_backends.AuthenticationBackend',  # Django-allauth backend
]

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
    'allauth.socialaccount.providers.github',
    'crispy_forms',
    'crispy_bootstrap4',
    'notifications',
    'sphere.apps.SphereConfig',
    'users.apps.UsersConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # Add the account middleware:
    "allauth.account.middleware.AccountMiddleware",
    'users.middleware.PreserveSessionMiddleware',
]


ROOT_URLCONF = 'blogsphere.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            # os.path.join(BASE_DIR, 'templates'),
            os.path.join(BASE_DIR, 'users', 'templates'),
            os.path.join(BASE_DIR, 'sphere', 'templates'),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.request',
            ],
        },
    },
]
# SOCIALACCOUNT_PROVIDERS = {}

SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'APP': {
            'client_id': config('SOCIAL_AUTH_GOOGLE_OAUTH2_KEY'),
            'secret': config('SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET'),
            'key': ''
        },
        'SCOPE': ['profile', 'email'],
        'AUTH_PARAMS': {'access_type': 'online'},
        'OAUTH_PKCE_ENABLED': True,
    },
    'github': {
        'APP': {
            'client_id': config('SOCIAL_AUTH_GITHUB_KEY'),
            'secret': config('SOCIAL_AUTH_GITHUB_SECRET'),
            'key': ''
        },
        'SCOPE': ['user:email'],
    }
}

WSGI_APPLICATION = 'blogsphere.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': config('DATABASE_NAME'),
        'USER': config('DATABASE_USER'),
        'PASSWORD': config('DATABASE_PASSWORD'),
        'HOST': config('DATABASE_HOST'),
        'PORT': config('DATABASE_PORT'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]

MEDIA_URL = 'media/'
# MEDIA_ROOT = BASE_DIR / 'media'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


CRISPY_TEMPLATE_PACK = 'bootstrap4'

LOGIN_REDIRECT_URL = 'sphere:home'
LOGIN_URL = 'account_login'

LOGOUT_REDIRECT_URL = 'account_login'
LOGOUT_URL = 'account_logout'
SIGNUP_URL = 'account_signup'
SIGNUP_REDIRECT_URL = 'account_login'
DEBUG_PROPAGATE_EXCEPTIONS = True


EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = config('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD')
DEFAULT_FROM_EMAIL = config('DEFAULT_FROM_EMAIL')
SILENCED_SYSTEM_CHECKS = ['models.W036']
MESSAGE_STORAGE = "django.contrib.messages.storage.cookie.CookieStorage"

# EMAIL_PORT = 465
# EMAIL_USE_TLS = False  # Set this to False for SSL
# EMAIL_USE_SSL = True   # Use SSL instead of TLS


ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_EMAIL_VERIFICATION = 'mandatory'  # For email verification (default setting)
ACCOUNT_EMAIL_CONFIRMATION_EXPIRE_DAYS = 3  # Set a valid number of days for email expiration
ACCOUNT_EMAIL_SUBJECT_PREFIX = '[users] '  # Customize the subject line

# settings.py
SESSION_ENGINE = "django.contrib.sessions.backends.db"
# SESSION_COOKIE_AGE = 1209600  # 2 weeks
SESSION_EXPIRE_AT_BROWSER_CLOSE = False
SESSION_SAVE_EVERY_REQUEST = True  # Ensure session is saved on each request
SESSION_COOKIE_AGE = 3600 * 24 * 7  # 1 week session
SESSION_COOKIE_NAME = 'blogsphere_session'


LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "file": {
            "level": "ERROR",
            "class": "logging.FileHandler",
            "filename": "errors.log",
        },
    },
    "loggers": {
        "django": {
            "handlers": ["file"],
            "level": "ERROR",
            "propagate": True,
        },
    },
}
