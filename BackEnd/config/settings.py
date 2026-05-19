"""
Django settings for config project — versione Windows-compatible.
"""

import pymysql
pymysql.install_as_MySQLdb()  # Usa PyMySQL al posto di mysqlclient

from pathlib import Path
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# ─── Sicurezza ──────────────────────────────────────────────────────────────
# Leggi da variabile d'ambiente in produzione; fallback solo in sviluppo locale
SECRET_KEY = os.environ.get(
    'SECRET_KEY',
    'django-insecure-%@7&e2y*-w6*=*ja-06)453ib91@ar68^lw5)n7%40jn=g8yhk'
)

DEBUG = True          # ← metti False in produzione
ALLOWED_HOSTS = ['localhost', '127.0.0.1']

# ─── App installate ──────────────────────────────────────────────────────────
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'corsheaders',
    'channels',
    'utenti',
    'componenti',
    'magazzino',
    'liste',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR.parent / 'FrontEnd'],

        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'

# ─── Database MySQL ───────────────────────────────────────────────────────────
# La password viene letta dalla variabile d'ambiente DB_PASSWORD;
# se non impostata, usa 'password' (solo sviluppo locale).
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'magazzino_fermi',
        'USER': 'root',
        'PASSWORD': os.environ.get('DB_PASSWORD', 'password'),
        'HOST': '127.0.0.1',   # su Windows '127.0.0.1' è più affidabile di 'localhost'
        'PORT': '3306',
        'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
            'charset': 'utf8mb4',
        },
    }
}

# ─── Validazione password ────────────────────────────────────────────────────
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# ─── JWT + DRF ───────────────────────────────────────────────────────────────
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
}

# ─── CORS ────────────────────────────────────────────────────────────────────
CORS_ALLOW_ALL_ORIGINS = True   # solo in sviluppo!

# ─── Channels (WebSocket) ────────────────────────────────────────────────────
ASGI_APPLICATION = 'config.asgi.application'
CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels.layers.InMemoryChannelLayer',
    },
}

# ─── Utente custom ───────────────────────────────────────────────────────────
AUTH_USER_MODEL = 'utenti.Utente'

# ─── Internazionalizzazione ──────────────────────────────────────────────────
LANGUAGE_CODE = 'it-it'
TIME_ZONE = 'Europe/Rome'
USE_I18N = True
USE_TZ = True

# ─── Static files ────────────────────────────────────────────────────────────
STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [BASE_DIR.parent / 'FrontEnd']
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'