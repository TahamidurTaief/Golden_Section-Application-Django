

from pathlib import Path
import os 

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-@r$t+bjg!1%ge(f&s!g4i4yrb&wdh0cob6)uy7^)hd*(_6c-**'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["*"]


# Custom User Model
AUTH_USER_MODEL = 'accounts.User'


# Application definition

INSTALLED_APPS = [
    'jazzmin',  # Must be before django.contrib.admin
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Third-party apps
    'ckeditor',
    'ckeditor_uploader',
    'imagekit',
    'django_extensions',
    'django_cotton',
    'django_tailwind_cli',
    'honeypot',
    'django_htmx',
    'django_browser_reload',

    # Your apps
    'accounts',
    'site_config',
    'categories',
    'services',
    'providers',
    'quotations',
    'content',
    'core',
    'bookings',
]


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    # 'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    
    'django_htmx.middleware.HtmxMiddleware',  # HTMX support
    'django_browser_reload.middleware.BrowserReloadMiddleware',  # Live reload
]



ROOT_URLCONF = 'GoldenSection.urls'



TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.media',
                'core.context_processors.site_settings',  # Site configuration
                'core.context_processors.navbar',  # Navbar categories
            ],
            'builtins': ['django_cotton.templatetags.cotton'],
        },
    },
]



WSGI_APPLICATION = 'GoldenSection.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True





STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    # "staticfiles": {
    #     "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    # },
}




# Default primary key field type
# https://docs.djangoproject.com/en/5.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'






# CSRF Trusted Origins - For POST requests from these domains
CSRF_TRUSTED_ORIGINS = [
    "http://localhost:8000",
    "http://127.0.0.1:8000",
    "https://alayla-issl.onrender.com/",
    "https://alayla.onrender.com",
    "https://alaylatourism.com",
]


# CSRF Cookie Settings
CSRF_COOKIE_SECURE = False  # Set to True in production with HTTPS
CSRF_COOKIE_HTTPONLY = False  # Allow JavaScript to read CSRF cookie if needed
CSRF_COOKIE_SAMESITE = 'Lax'  # 'Lax', 'Strict', or 'None'
CSRF_USE_SESSIONS = False  # Use cookies instead of sessions for CSRF token

# Session Cookie Settings
SESSION_COOKIE_SECURE = False  # Set to True in production with HTTPS
SESSION_COOKIE_HTTPONLY = True  # Prevent JavaScript from accessing session cookie
SESSION_COOKIE_SAMESITE = 'Lax'

# Security Headers (for production)
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'SAMEORIGIN'  # Allow framing from same origin


# Security Settings
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'
CSRF_COOKIE_SECURE = False  # Set True in production with HTTPS
SESSION_COOKIE_SECURE = False  # Set True in production with HTTPS
SECURE_SSL_REDIRECT = False  # Set True in production with HTTPS

# Honeypot settings
HONEYPOT_FIELD_NAME = 'email_confirm'

# For browser reload
INTERNAL_IPS = ["127.0.0.1"]

# Anti-spam honeypot
HONEYPOT_FIELD_NAME = 'email_confirm'







# ImageKit Configuration
IMAGEKIT_DEFAULT_CACHEFILE_BACKEND = 'imagekit.cachefiles.backends.Simple'
IMAGEKIT_CACHEFILE_DIR = 'CACHE/images'
IMAGEKIT_DEFAULT_FILE_STORAGE = 'django.core.files.storage.FileSystemStorage'
IMAGEKIT_SPEC_CACHEFILE_NAMER = 'imagekit.cachefiles.namers.source_name_as_path'

# CKEditor Configuration
CKEDITOR_UPLOAD_PATH = "uploads/"
CKEDITOR_IMAGE_BACKEND = "pillow"
CKEDITOR_JQUERY_URL = 'https://ajax.googleapis.com/ajax/libs/jquery/3.6.0/jquery.min.js'

CKEDITOR_CONFIGS = {
    'default': {
        'skin': 'moono-lisa',
        'toolbar_Basic': [
            ['Source', '-', 'Bold', 'Italic']
        ],
        'toolbar_Full': [
            ['Styles', 'Format', 'Bold', 'Italic', 'Underline', 'Strike', 'SpellChecker', 'Undo', 'Redo'],
            ['Link', 'Unlink', 'Anchor'],
            ['Image', 'Flash', 'Table', 'HorizontalRule'],
            ['TextColor', 'BGColor'],
            ['Smiley', 'SpecialChar'], ['Source'],
            ['JustifyLeft', 'JustifyCenter', 'JustifyRight', 'JustifyBlock'],
            ['NumberedList', 'BulletedList'],
            ['Indent', 'Outdent'],
            ['Maximize'],
        ],
        'toolbar': 'Full',
        'height': 300,
        'width': '100%',
        'filebrowserWindowWidth': 940,
        'filebrowserWindowHeight': 725,
        'allowedContent': True,  # Allow all HTML content
        'extraAllowedContent': 'div(*);p(*);span(*);a[*];img[*];h1;h2;h3;h4;h5;h6',  # Allow additional tags with HTMX attributes
        'forcePasteAsPlainText': False,
        'removePlugins': '',
        'extraPlugins': 'divarea,dialog,dialogui',
    },
    'awesome_ckeditor': {
        'toolbar': 'Full',
        'height': 400,
        'allowedContent': True,
        'extraAllowedContent': 'div(*);p(*);span(*);a[*];img[*];button[*];form[*];input[*]',  # Full HTMX support
    },
}
