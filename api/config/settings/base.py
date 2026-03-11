from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/6.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-mid%3&ff()0j^p^85ck)eq65!ei)dhmbp9uzlbx1q@8m2&k+op'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []



# Application definition

INSTALLED_APPS = [
    'apps.users',
    'apps.products',
    'apps.cart',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'django_filters',
    'drf_spectacular',
]

MIDDLEWARE = [
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
        'DIRS': [],
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

#----------------------------------
from datetime import timedelta

# 1 Tell Django to Use This User Model Instead of the Default One
AUTH_USER_MODEL = "users.User"

# 2 Configure DRF + JWT
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
    "DEFAULT_PERMISSION_CLASSES": (
        "rest_framework.permissions.IsAuthenticated",
    ),
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": 10,
    "DEFAULT_FILTER_BACKENDS": [
        "django_filters.rest_framework.DjangoFilterBackend",
        "rest_framework.filters.SearchFilter",
        "rest_framework.filters.OrderingFilter",
    ],
    
}
# ⚙️ JWT Token Configuration in Django settings.py
# This controls how long authentication tokens remain valid

SIMPLE_JWT = {
    # 🕐 Access Token Lifetime
    # This is the token used for API requests (sent in Authorization header)
    # After this time, the token expires and cannot be used anymore
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=30),  # Default is 5 minutes
    
    # 🔄 Refresh Token Lifetime
    # This token is used to get new access tokens without re-login
    # It lives longer than access token
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),     # Default is 1 day
    
    # 🔁 Token Rotation Settings
    'ROTATE_REFRESH_TOKENS': True,   # Get new refresh token when refreshing
    'BLACKLIST_AFTER_ROTATION': True, # Old refresh tokens become invalid
    
    # 🔐 Security Settings
    'UPDATE_LAST_LOGIN': False,       # Don't update last_login on each token refresh
    
    # 🎯 Algorithm Settings
    'ALGORITHM': 'HS256',              # Encryption algorithm for tokens
    'SIGNING_KEY': 'your-secret-key-here', # Secret key to sign tokens
    
    # 📝 Header Settings
    'AUTH_HEADER_TYPES': ('Bearer',),  # Token type in Authorization header
                                       # Example: "Authorization: Bearer <token>"
    
    # 👤 User Identification
    'USER_ID_FIELD': 'id',              # Which field identifies the user
    'USER_ID_CLAIM': 'user_id',         # Name of the claim in token payload
}

# 📝 What the tokens contain (payload example):
# {
#   "user_id": 123,
#   "exp": 1678901234,  # Expiration timestamp
#   "iat": 1678900034,  # Issued at timestamp
#   "token_type": "access"  # Type of token
# }


MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

#----------------------------------

# Database
# https://docs.djangoproject.com/en/6.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/6.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/6.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/6.0/howto/static-files/

STATIC_URL = 'static/'
