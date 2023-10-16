from pathlib import Path
import environ

# Значения переменных окружения по умолчанию
env = environ.Env(
    SECRET_KEY=(str, '*'),
    DEBUG=(bool, True),
    ALLOWED_HOSTS=(list, []),
    DB_NAME=str,
    POSTGRES_USER=str,
    POSTGRES_PASSWORD=str,
    DB_HOST=str,
    DB_PORT=int,
)
# Чтение переменных окружения из файла .env
environ.Env.read_env()

# Абсолютный путь до корня проекта
BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = env('SECRET_KEY')

DEBUG = env('DEBUG')
# Имена хостов/доменов, которые может обслуживать приложение:
ALLOWED_HOSTS = env.list('ALLOWED_HOSTS')

# Список установленных приложений
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'djoser',
    'users.apps.UsersConfig',
    'ingredients.apps.IngredientsConfig',
    'recipes.apps.RecipesConfig',
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
# Путь к корневой конфигурации URL
ROOT_URLCONF = 'backend.urls'

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
# Путь к конфигурации WSGI
WSGI_APPLICATION = 'backend.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': env('DB_NAME'),
        'USER': env('POSTGRES_USER'),
        'PASSWORD': env('POSTGRES_PASSWORD'),
        'HOST': env('DB_HOST'),
        'PORT': env('DB_PORT'),
    }
}
# Проверка паролей пользователей
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
# Язык в приложении
LANGUAGE_CODE = 'ru-RU'

# Часовой пояс для базы данных
TIME_ZONE = 'UTC'

# Перевод языка
USE_I18N = False

# Чтение даты и времени из базы данных возвращает дату и время в текущем часовом поясе вместо UTC
USE_TZ = True

# URL-адрес, который будет использоваться при ссылке на статические файлы, расположенные в STATIC_ROOT
STATIC_URL = 'static/'

# Абсолютный путь к каталогу, в котором Collectstatic будет собирать статические файлы для развертывания
STATIC_ROOT = BASE_DIR.joinpath('static')

# URL-адрес, который обрабатывает медиафайлы, передаваемые из MEDIA_ROOT
MEDIA_URL = '/media/'

# Абсолютный путь к каталогу, в котором будут храниться загруженные медиа-файлы
MEDIA_ROOT = BASE_DIR.joinpath('media')

# Тип поля первичного ключа по умолчанию, используемый для моделей, у которых нет поля с Primary_key=True
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Модель, используемая для представления пользователя
AUTH_USER_MODEL = 'users.User'
