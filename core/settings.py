from pathlib import Path
from django.conf import settings
import pdfkit
import os
from .jazzmin import JAZZMIN_SETTINGS
BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY ='django-insecure-mu%o*!555_3i#ohr_9bvnr!pr-#z^spial)**uboqy&ixqnkkd'
DEBUG = True
ALLOWED_HOSTS = ['*']

INSTALLED_APPS = [
    'jazzmin',
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    'rest_framework',
    'crispy_forms',
    'crispy_bootstrap4',

    "course",
    'users',
    'main',
    'payment',
    'api',
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "core.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR.joinpath('templates')],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
               #'main.views.base',
              
            ],
        },
    },
]

WSGI_APPLICATION = "core.wsgi.application"


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite4",
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = "uz"

TIME_ZONE = "Asia/Tashkent"

USE_I18N = True

USE_TZ = True

CRISPY_TEMPLATE_PACK = "bootstrap4"
CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap4"
# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = "static/"
STATICFILES_DIRS = [str(BASE_DIR.joinpath('static'))]
STATIC_ROOT = str(BASE_DIR.joinpath('staticfiles')) 
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
AUTH_USER_MODEL = 'users.User'
LOGOUT_REDIRECT_URL = 'index'
LOGIN_REDIRECT_URL = 'index'

# settings.pyPDFKIT_CONFIG = pdfkit.configuration(wkhtmltopdf=r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe')

JAZZMIN_SETTINGS = JAZZMIN_SETTINGS

JAZZMIN_UI_TWEAKS = {
    "theme": "flatly",  # Apply a classic light theme
    "navbar": "navbar-light navbar-light",  # Light navbar color
    "no_navbar_border": True,  # Remove navbar border
    "sidebar": "sidebar-light-primary",  # Light sidebar color
    "brand_small_text": False,  # Use small text for brand
    "footer_fixed": True,  # Fix footer
    "body_small_text": False,  # Use small text in body
    "sidebar_nav_small_text": False,  # Use small text in sidebar
    "sidebar_disable_expand": False,  # Disable sidebar expand/collapse
    "sidebar_nav_child_indent": False,  # Indent child menu items in sidebar
    "sidebar_nav_compact_style": True,  # Compact sidebar style
    "sidebar_nav_flat_style": False,  # Flat sidebar style
    "theme_switcher": False,  # Disable theme switcher
}


EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'  # Example: 'smtp.gmail.com'
EMAIL_PORT = 587  # Use the appropriate port for your email provider
EMAIL_USE_TLS = True  # True for most providers, False if not using TLS/SSL
EMAIL_HOST_USER = 'mritacademy01@gmail.com'  # Replace with your email address
EMAIL_HOST_PASSWORD = 'jevu cugp knvw whdr'
EMAIL_DEBUG = True


