"""
Django settings for luffycityapi project.

Generated by 'django-admin startproject' using Django 4.1.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""

import sys
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# sys.path.insert(0, 'luffycityapi/apps')
sys.path.insert(0, str(BASE_DIR / 'apps'))
sys.path.insert(0, str(BASE_DIR / 'utils'))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-c@c@$(1)zocl++2o7a&ml6b=co(7dv2!u!#n9d6+sde$y83u+j'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["*"]

# Application definition

INSTALLED_APPS = [
    'simpleui',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'rest_framework',
    'corsheaders',
    'ckeditor',
    'ckeditor_uploader',
    'stdimage',

    'home',
    'users',
    'courses',
]

CORS_ORIGIN_ALLOW_ALL = True

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    # 'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'luffycityapi.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'luffycityapi.wsgi.application'

# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'luffycity',
        'USER': 'caoruchen',
        'PASSWORD': 'crc',
        'HOST': 'localhost',
        'PORT': '3306',
        'POOL_OPTIONS': {
            'pool_size': 10,
            'max_overflow': 50,
        }
    }
}

CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://:@127.0.0.1:6379/0',
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
            'CONNECTION_POOL_KWARGS':{
                'max_connections': 100,
            }
        }
    },
    'session': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://:@127.0.0.1:6379/1',
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
            'CONNECTION_POOL_KWARGS':{
                'max_connections': 100,
            }
        }
    },
    'sms_code': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://:@127.0.0.1:6379/2',
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
            'CONNECTION_POOL_KWARGS':{
                'max_connections': 100,
            }
        }
    }
}

SESSION_ENGINE = 'django.contrib.sessions.backends.cache'
SESSION_CACHE_ALIAS = 'session'

# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = 'zh-hans'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = 'static/'
STATICFILES_DIRS = (
    BASE_DIR / 'static',
)

MEDIA_ROOT = BASE_DIR / 'uploads'
MEDIA_URL = '/uploads/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'simple': {
            'format': '{levelname} {asctime} {module} {message}',
            'style': '{',
        },
        'verbose': {
            'format': '{levelname} {message}',
            'style': '{',
        }
    },
    'filters':{
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        }
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
            'filters': ['require_debug_true'],
            'level': 'DEBUG',
        },
        'file': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'formatter': 'verbose',
            'filename': BASE_DIR.parent / 'logs' / 'luffycity.log',
            'maxBytes': 1024 * 1024 * 300,
            'backupCount': 10,
        }
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'file'],
            'propagate': True,
        }
    }
}

################# settings below are manually added to REST_FRAMEWORK #################
REST_FRAMEWORK = {
    'EXCEPTION_HANDLER': 'luffycityapi.utils.exceptions.custom_exception_handler',
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_jwt.authentication.JSONWebTokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
    )
}

import datetime
# jwt认证相关配置项
JWT_AUTH = {
    # 设置jwt的有效期
    'JWT_EXPIRATION_DELTA': datetime.timedelta(weeks=1), # 一周有效，
    'JWT_PAYLOAD_HANDLER': 'luffycityapi.utils.authenticate.jwt_payload_handler',
}

AUTH_USER_MODEL = "users.User"
AUTHENTICATION_BACKENDS = ('luffycityapi.utils.authenticate.CustomAuthBackend', )

# CKEDITOR configurations
# 上传文件的存储路径
CKEDITOR_UPLOAD_PATH = "ckeditor/"

# 工具条配置
CKEDITOR_CONFIGS = {
    'default': {
        # 'toolbar': 'full', # full 显示全部工具
        # 'toolbar': 'Basic', # Basic 显示基本工具
        'toolbar': 'Custom',  # 自定义工具条的显示数量
        'toolbar_Custom': [
            ['Bold', 'Italic', 'Underline', 'Image', 'Styles', 'Format', 'Font', 'Fontsize'],
            ['NumberedList', 'BulletedList', '-', 'Outdent', 'Indent', '-', 'JustifyLeft', 'JustifyCenter',
             'JustifyRight', 'JustifyBlock'],
            ['Link', 'Unlink', 'Table'],
            ['RemoveFormat', 'Source']
        ],
        # 设置编辑器的高度
        'height': 120,
    },
}

# admin site UI configurations
from django.contrib import admin
admin.AdminSite.site_header = 'caoruchen online education'
admin.AdminSite.site_title = 'crc online admin management'

# 登录界面logo
SIMPLEUI_LOGO = '/uploads/logo.png'
# 快速操作
SIMPLEUI_HOME_QUICK = True
# 服务器信息
SIMPLEUI_HOME_INFO = True

# 关闭simpleui内置的使用分析
SIMPLEUI_ANALYSIS = False
# 离线模式
SIMPLEUI_STATIC_OFFLINE = True
# 首页图标地址
SIMPLEUI_INDEX = 'http://www.luffycity.cn:3000/'
