# Foodgram
Онлайн сервис, на котором пользователи могут оставлять рецепты, подписываться на других авторов, добавлять рецепты в «Избранное», а перед походом в магазин скачивать список продуктов, необходимых для приготовления одного или нескольких выбранных блюд
## Запустить проект с помощью Docker
1) Клонируйте репозиторий 
```
git clone https://github.com/cyberdas/foodgram-project
```
2) В директории foodgram создайте файл .env с переменным окружения (в качестве примера можно использовать эти)
- POSGRES_DB=foodgram
- POSTGRES_USER=foodgramuser
- POSTGRES_PASSWORD=123456
- DB_HOST=db
- DB_PORT=5432
3) Разверните проект с помощью docker-compose
```
docker-compose up --build
```
4) В окне терминала войдите в контейнер web
```
docker exec -it <CONTAINER_ID> bash
```
5) В контейнере выполните миграции, создайте суперпользователя:
```
python manage.py migrate

python manage.py createsuperuser
```
6) Также есть возможность загрузить стартовые данные из файла dump.json
```
python manage.py shell 
# выполнить в открывшемся терминале:
>>> from django.contrib.contenttypes.models import ContentType
>>> ContentType.objects.all().delete()
>>> quit()
python manage.py loaddata dump.json

```
