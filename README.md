##HR-Site
**Создайте образ:**
```
$ docker-compose build 
```
**После создания образа запустите контейнер:**
```
$ docker-compose up -d 
```

**Переходим в контейнер**
```
docker exec -it home_db_1 bash
psql -U postgres
ALTER USER postgres WITH ENCRYPTED PASSWORD 'Asasa2121q';
\q
exit
```
**Удаляем что хотим**
```
docker stop $(docker ps -a -q)
docker rm $(docker ps -a -q)
docker rmi $(docker images -a -q)
```
**ЧТО БУДУ ИСПОЛЬЗОВАТЬ**
```
django-push-notifications
```

**Список томов**
```
docker volume ls
```

**Удаление тома**
```
docker volume rm home_postgres_data
```
