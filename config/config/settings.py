import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.environ.get('SECRET_KEY')

DEBUG = True

ALLOWED_HOSTS = [os.environ.get('ALLOWED_HOSTS')]


INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    'django.contrib.sites',
    'channels',
    'chat',
    'django.contrib.flatpages',

    'crispy_forms',
    'ckeditor',
    'ckeditor_uploader',
    'app_account',
    'app_flatpage',
    'app_profile',
    'app_main',
    'import_export',
    'django_user_agents',
    'email_sender.apps.EmailSenderConfig',

    "debug_toolbar",
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
"debug_toolbar.middleware.DebugToolbarMiddleware",
    'django_user_agents.middleware.UserAgentMiddleware',

]

ROOT_URLCONF = 'config.urls'

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
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'

ASGI_APPLICATION = 'config.asgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('DB_NAME'),
        'USER': os.environ.get('DB_USER'),
        'PASSWORD': os.environ.get('DB_PASSWORD'),
        'HOST': os.environ.get('DB_HOST'),
        'PORT': os.environ.get('DB_PORT', '5432'),
    }
}

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

LANGUAGE_CODE = 'ru'

TIME_ZONE = 'Europe/Moscow'

USE_I18N = True

USE_L10N = True

USE_TZ = True

STATIC_URL = '/static/'

STATIC_ROOT = BASE_DIR.parent / "staticfiles"

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)
MEDIA_URL = '/media/'

MEDIA_ROOT = BASE_DIR.parent / "media"

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTH_USER_MODEL = 'app_account.User'

TELPHIN_APP_ID = os.environ.get('TELPHIN_APP_ID')

TELPHIN_APP_SECRET = os.environ.get('TELPHIN_APP_SECRET')

TELPHIN_URL_ONE = 'https://flashcall.telphin.ru/'

TELPHIN_URL_TWO = 'https://flashcall.telphin.ru/auth/'

LOGIN_REDIRECT_URL = '/'
LOGIN_URL = '/'
SITE_ID = 1

CRISPY_TEMPLATE_PACK = 'bootstrap4'
CKEDITOR_UPLOAD_PATH = "uploads/"

CKEDITOR_CONFIGS = {
    'default': {
        'allowedContent': True,
        'skin': 'moono',
        'toolbar_Basic': [
            ['Source', '-', 'Bold', 'Italic']
        ],
        'toolbar_YourCustomToolbarConfig': [
            {'name': 'document', 'items': ['Source', '-', 'Save', 'NewPage', 'Preview', 'Print', '-', 'Templates']},
            '/',
            {'name': 'basicstyles',
             'items': ['Bold', 'Italic', 'Underline', 'Strike', 'Subscript', 'Superscript', '-', 'RemoveFormat']},

            {
                "name": "widgets",
                "items": [
                    "Undo",
                    "Redo",
                    "-",
                    "NumberedList",
                    "BulletedList",
                    "-",
                    "Outdent",
                    "Indent",
                    "-",
                    "Link",
                    "Unlink",
                    "-",
                    "Image",
                    "CodeSnippet",
                    "Table",
                    "HorizontalRule",
                    "Smiley",
                    "SpecialChar",
                    "-",
                    "Blockquote",
                    "-",
                    "ShowBlocks",
                    "Maximize",
                ],
            },
            {'name': 'paragraph',
             'items': ['NumberedList', 'BulletedList', '-', 'Outdent', 'Indent', '-', 'Blockquote', 'CreateDiv', '-',
                       'JustifyLeft', 'JustifyCenter', 'JustifyRight', 'JustifyBlock']},
            '/',
            {'name': 'styles', 'items': ['Styles', 'Format', 'Font', 'FontSize', 'MyStyle']},
            {'name': 'colors', 'items': ['TextColor', 'BGColor']},
            {'name': 'tools', 'items': ['Maximize', 'ShowBlocks']},

            '/',  # put this to force next toolbar on new line
            {'name': 'yourcustomtools', 'items': [
                # put the name of your editor.ui.addButton here
                'Preview',
                'Maximize',

            ]},
        ],
        'toolbar': 'YourCustomToolbarConfig',  # put selected toolbar config here

        'width': '100%',

        'tabSpaces': 4,
        'extraPlugins': ','.join([
            'uploadimage', # the upload image feature
            'div',
            'autolink',
            'autoembed',
            'embedsemantic',
            'autogrow',
            'widget',
            'lineutils',
            'clipboard',
            'dialog',
            'dialogui',
            'elementspath'

        ]),
    }
}

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': '127.0.0.1:11211',
    }
}

USER_AGENTS_CACHE = 'default'

CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            "hosts": [('redis', 6379)],
        },
    },
}

EMAIL_HOST = 'smtp.jino.ru'
EMAIL_HOST_USER = 'post@vahtoweek.ru'
DEFAULT_FROM_EMAIL = 'post@vahtoweek.ru'
EMAIL_HOST_PASSWORD = 'qwerty123123!'
EMAIL_PORT = 587
EMAIL_USE_TLS = True


SMS_RU_APP_ID = os.environ.get('SMS_RU_APP_ID')
SMS_RU_URL = 'https://sms.ru/code/call'

if DEBUG:
    def show_toolbar(request):
        return True
    DEBUG_TOOLBAR_CONFIG = {
        "SHOW_TOOLBAR_CALLBACK" : show_toolbar,
    }
