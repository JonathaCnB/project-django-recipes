from pathlib import Path

from decouple import config

BASE_DIR = Path(__file__).resolve().parent.parent.parent

SECRET_KEY = config("SECRET_KEY")

DEBUG = config("DEBUG", default=False, cast=bool)

ALLOWED_HOSTS = config("ALLOWED_HOSTS").split(" ")

ROOT_URLCONF = "project.urls"

WSGI_APPLICATION = "project.wsgi.application"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

SITE_ID = 1

SELENIUM_HEADLESS = config("SELENIUM_HEADLESS", default=False, cast=bool)

PER_PAGES = config("PER_PAGES", default=6, cast=int)
