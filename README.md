# Шпарглка Poetry, Django, Nginx, Postgres, Docker     

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
```bash
poetry export -f requirements.txt > app/requirements.txt
```

При первом запуске контейнера: 
1. Запустить миграцию
2. Потом создать ```schema``` ```content```
3. Еще раз запустиь миграцию
4. Cоздать суперпользователя 

Примеры команд 
```bash
docker exec -it <container_id_or_name> python manage.py migrate
docker exec -it <container_id_or_name> python manage.py createsuperuser
```

PS При деплое не забываем раскометировать блоки кода в .env файле

##### TODO 
- Схему(schema) нужно создавть при деплое
- Часто используемые команды попробовать перенести в Poetry scripts
- При создании ```sh``` файлов в windows получатся не приятность как ее пофиксить можно прочитать [тут](https://futurestud.io/tutorials/how-to-fix-exec-user-process-caused-no-such-file-or-directory-in-docker) 

