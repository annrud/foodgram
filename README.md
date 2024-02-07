# Foodgram

## Описание
Приложение **Foodgram** или **"Продуктовый помощник"** - дипломный проект, созданный в рамках программы 
обучения на курсе **GeekBrains «Программист python. Цифровые профессии».**

**"Продуктовый помощник"** - сервис для обмена рецептами приготовления различных блюд. 
Пользователи публикуют свои рецепты, подписываются на других пользователей, 
добавляют понравившиеся рецепты в «Избранное» и «Список покупок». Реализована возможность скачивания списка продуктов, 
необходимых для приготовления блюд, добавленных в «Список покупок» в формате txt.*<br>

В проекте реализованы backend и API в соответствии с документацией reDoc. 
Для работы использовался готовый frontend на React. Макет приложения доступен на <a href="https://www.figma.com/file/HHEJ68zF1bCa7Dx8ZsGxFh/%D0%9F%D1%80%D0%BE%D0%B4%D1%83%D0%BA%D1%82%D0%BE%D0%B2%D1%8B%D0%B9-%D0%BF%D0%BE%D0%BC%D0%BE%D1%89%D0%BD%D0%B8%D0%BA-(Final)?node-id=0%3A1">Figma.com</a>.<br>

## Технологии:
- Python 3.10
- Django 4.2.4
- Django REST Framework 3.14.0
- PostgreSQL 12.4
- Docker Compose 3.8
- Gunicorn 21.2.0
- Nginx 1.25.1

## Этапы запуска приложения на локальной машине:
1. Установите <a href=https://docs.docker.com/engine/install/ubuntu/>docker</a>
2. Клонируйте проект в рабочую директорию:<br> 
```$ git clone https://github.com/<ваш_username>/foodgram.git```
3. Создайте файл .env (в директории backend/foodgram рядом с settings.py) с переменными окружения:<br> 
DB_ENGINE, DB_NAME, POSTGRES_USER, POSTGRES_PASSWORD, DB_HOST, DB_PORT, SECRET_KEY, DEBUG, ALLOWED_HOSTS<br>
4. Создание сервисов (выполнение команды из корневой папки):
```$ docker compose -f infra/docker-compose.yml build```<br>
5. Сборка и запуск контейнеров:<br>
```$ docker compose -f infra/docker-compose.yml up -d```<br>
6. Вход внутрь контейнера backend и выполнение миграций:<br>
```$ docker-compose -f infra/docker-compose.yml exec backend sh```
```# python manage.py migrate```<br>
7. Создание суперпользователя (команда выполняется внутри контейнера backend):<br>
```# python manage.py createsuperuser```<br>
8. Заполнение базы данных начальными данными (ингредиенты и их единицы измерения):<br>
```# python manage.py load_data```<br>
9. Проект доступен локально: http://localhost:80/ <br>
10. Админка: http://localhost/admin/ <br>
11. Спецификация API располагается по адресу http://localhost/api/docs/ <br>

### Дополнительные команды:<br>
Остановка и удаление контейнеров: ```docker compose -f infra/docker-compose.yml down```<br>
Просмотр логов: ```docker compose -f infra/docker-compose.yml logs```<br>

## Разработчик:
<a href="https://github.com/annrud">*Попова Анна*</a>
