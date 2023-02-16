import os

from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent


# Quick-start development settings - unsuitable for production

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure--31r7+vtd8!c5h79s+=m4&yd7x*_wwoo$4#w(xr%)lfvwr*)4g"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    
    "django_htmx",
    "widget_tweaks",
    
    "alert",
    "account",
    "newsletter",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "django_htmx.middleware.HtmxMiddleware",
]

ROOT_URLCONF = "core.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "account.context_processors.account",
                "newsletter.context_processors.newsletter",
            ],
        },
    },
]

WSGI_APPLICATION = "core.wsgi.application"


# Database

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}


# Password validation

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

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)

STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")
STATIC_URL = 'static/'

STATIC_DIR = os.path.join(BASE_DIR, 'static')
STATICFILES_DIRS = [STATIC_DIR, ]

MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media/")
# Default primary key field type

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


AUTH_USER_MODEL = "account.Customer"

LOGIN_REDIRECT_URL = "account:dashboard"

LOGIN_URL = "account:login"

EMAIL_HOST_USERNAME = "Admin@cozastore.com"


# # Stripe settings

# STRIPE_TEST_PUBLIC_KEY ='pk_test_51LkTclEuBM4N6BqzT03vDUYZom2Ndznfo8GK3LpR3fP9UPPhvYXoxVD5RKjHIKn5OaftnLHMsEeF6xys8xKJCoS300f4ETu5GZ' # add here
# STRIPE_TEST_SECRET_KEY ='sk_test_51LkTclEuBM4N6BqzqXeh2JulBstWuAvM7nbQrkkojnCLulExtpLNosMuPPBHh5PWSkZayMPAopWFWBXJ5YA5fHqP00Z5WgEn4j' # add here
# STRIPE_LIVE_MODE = False  # Change to True in production

# # Add these two lines even if you are not using webhooks
# DJSTRIPE_WEBHOOK_SECRET = "whsec_xxx"
# DJSTRIPE_FOREIGN_KEY_TO_FIELD = "id"