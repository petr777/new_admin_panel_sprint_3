# Шпарглка Poetry, Django, Nginx, Postgres, Docker, Elastic     

#### Клонируем репозиторий

```bash
git clone https://github.com/petr777/new_admin_panel_sprint_2.git
```

Cоздаем виртуальное окружение и устанавливаем необходимые зависимости
```bash
poetry shell
poetry install
```


При запуске вебсервера в процессе разработки можно запустить отдельно контейнер с ```Postgres```
```bash
docker-compose up -d db
```
ну и соответственно использовать встроенный в ```django``` сервер 

Запускаем сервисы 
```bash
docker-compose up -d --build
```

## deploy
Собрать актульный ```requirements.txt``` 

для django приложения 
```bash
poetry export -f requirements.txt > app/requirements.txt
```

для etl нужно оставиь только те зависимости которые нужны именно этому сервису 
```bash
poetry export -f requirements.txt > pg_to_es/requirements.txt
```


При первом запуске контейнера:
1. Cоздать суперпользователя 
2. При запуске сразу всех сервисов, не успевает создваться нужная схема и данные начинают сразу синхронизироваться
нужно что-то придумать по этому поводу, пока тормозим сервис etl_postgre_to_elkastic, далее создаем схему 
см. папку `dev` после удалемм файл LocalStorege в

```bash
rm storage.json
```
3. После удаления файла синхронизация начнется заново.
4. Запускаем Postman тесты.


Примеры команд 
```bash
docker exec -it <container_id_or_name> python manage.py migrate
docker exec -it <container_id_or_name> python manage.py createsuperuser
```

PS При деплое не забываем раскометировать блоки кода в .env файле

##### TODO 
- Схему(schema) нужно создавть при деплое как для Postgres так и для Elasticsearch.
- Часто используемые команды попробовать перенести в Poetry scripts
- При создании ```sh``` файлов в windows получатся не приятность как ее пофиксить можно прочитать [тут](https://futurestud.io/tutorials/how-to-fix-exec-user-process-caused-no-such-file-or-directory-in-docker) 

