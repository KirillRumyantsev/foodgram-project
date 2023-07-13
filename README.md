# Проект «Продуктовый помощник» - Foodgram
Foodgram - Продуктовый помощник. Сервис позволяет публиковать рецепты, подписываться на публикации других пользователей, добавлять понравившиеся рецепты в список "Избранное", а перед походом в магазин - скачивать сводный список продуктов, необходимых для приготовления одного или нескольких выбранных блюд.

## Стек технологий
[![Python](https://img.shields.io/badge/-Python-464646?style=flat&logo=Python&logoColor=56C0C0&color=008080)](https://www.python.org/)
[![Django](https://img.shields.io/badge/-Django-464646?style=flat&logo=Django&logoColor=56C0C0&color=008080)](https://www.djangoproject.com/)
[![Django REST Framework](https://img.shields.io/badge/-Django%20REST%20Framework-464646?style=flat&logo=Django%20REST%20Framework&logoColor=56C0C0&color=008080)](https://www.django-rest-framework.org/)
[![PostgreSQL](https://img.shields.io/badge/-PostgreSQL-464646?style=flat&logo=PostgreSQL&logoColor=56C0C0&color=008080)](https://www.postgresql.org/)
[![Nginx](https://img.shields.io/badge/-NGINX-464646?style=flat&logo=NGINX&logoColor=56C0C0&color=008080)](https://nginx.org/ru/)
[![gunicorn](https://img.shields.io/badge/-gunicorn-464646?style=flat&logo=gunicorn&logoColor=56C0C0&color=008080)](https://gunicorn.org/)
[![Docker](https://img.shields.io/badge/-Docker-464646?style=flat&logo=Docker&logoColor=56C0C0&color=008080)](https://www.docker.com/)
[![Docker-compose](https://img.shields.io/badge/-Docker%20compose-464646?style=flat&logo=Docker&logoColor=56C0C0&color=008080)](https://www.docker.com/)
[![GitHub%20Actions](https://img.shields.io/badge/-GitHub%20Actions-464646?style=flat&logo=GitHub%20actions&logoColor=56C0C0&color=008080)](https://github.com/features/actions)
[![Yandex.Cloud](https://img.shields.io/badge/-Yandex.Cloud-464646?style=flat&logo=Yandex.Cloud&logoColor=56C0C0&color=008080)](https://cloud.yandex.ru/)

### Workflow
* build_and_push_to_docker_hub - Сборка и доставка докер-образов на Docker Hub
* deploy - Автоматический деплой проекта на боевой сервер. Выполняется копирование файлов из репозитория на сервер:
В репозитории на Гитхабе добавьте данные в **`Settings - Secrets - Actions secrets`**:
- ```DOCKER_USERNAME``` - имя пользователя в DockerHub
- ```DOCKER_PASSWORD``` - пароль пользователя в DockerHub
- ```HOST``` - адрес сервера
- ```USER``` - пользователь
- ```SSH_KEY``` - приватный ssh ключ
- ```SSH_PASSPHRASE``` - кодовая фраза для ssh-ключа
При внесении любых изменений в проект, после коммита и пуша
```
git add .
git commit -m "..."
git push
```
запускается набор блоков команд jobs т.к. команда `git push` является триггером workflow проекта.

## Установка Docker (на платформе Ubuntu)

Проект поставляется в четырех контейнерах Docker (db, frontend, backend, nginx).  
Для запуска необходимо установить Docker и Docker Compose.  
Подробнее об установке на других платформах можно узнать на [официальном сайте](https://docs.docker.com/engine/install/).

Для начала необходимо скачать и выполнить официальный скрипт:
```bash
apt update
apt install curl
curl -fsSL https://get.docker.com -o get-docker.sh
sh ./get-docker.sh
```

Установить Docker(CE) и Docker Compose:
```bash
apt install docker-ce docker-compose -y
```

Проверить что  Docker работает можно командой:
```bash
systemctl status docker
```

Подробнее об установке можно узнать по [ссылке](https://docs.docker.com/engine/install/ubuntu/).

## База данных и переменные окружения

Проект использует базу данных PostgreSQL.  
Для подключения и выполненя запросов к базе данных необходимо создать и заполнить файл ".env" в корневой папке проекта.

Шаблон для заполнения файла ".env.example":
```python
SECRET_KEY
DEBUG
ALLOWED_HOSTS
PG_DATABASE
PG_USER
PG_PASSWORD
PG_HOST
PG_PORT
```

## Запуск контейнеров

Для запуска контейнеров в корневой папке проекта необходимо создать и заполнить файл docker-compose.yml, содержимое файла можно взять тут
```bash
foodgram-project-react/infra/
```

Запустить контейнеры в режиме демона.

Из папки в которой находится файл docker-compose.yml выполнить команду:
```bash
sudo docker compose -f docker-compose.yml up -d
```

Проверьте, что все нужные контейнеры запущены:
```bash
sudo docker compose -f docker-compose.production.yml ps
```

Выполните миграции, соберите статические файлы бэкенда и скопируйте их в /backend_static/static/:
```bash
sudo docker compose -f docker-compose.production.yml exec backend python manage.py migrate
sudo docker compose -f docker-compose.production.yml exec backend python manage.py collectstatic
sudo docker compose -f docker-compose.production.yml exec backend cp -r /app/collected_static/. /backend_static/static/
```

## Заполнение базы данных

С проектом поставляются данные об ингредиентах.  
Заполнить базу данных ингредиентами можно выполнив следующую команду из корневой папки проекта
```bash
sudo docker compose -f docker-compose.yml exec backend python manage.py load_data
```

Также необходимо заполнить базу данных тегами (или другими данными).  
Для этого требуется войти в [админ-зону](http://localhost/admin/)
проекта под логином и паролем администратора (пользователя, созданного командой createsuperuser).
