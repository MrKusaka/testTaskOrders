# testTaskOrders

Приложение для создания заказов на основе FastAPI

Приложение написано на версии python 3.10.4, с установкой на версию выше могут возникать проблемы

### Запуск в docker

1. Поставьте [Docker](https://www.docker.com/get-started)

2. Клонируйте репозиторий:

```bash
git clone https://github.com/MrKusaka/testTaskOrders.git
cd testTaskOrders
python -m venv venv
. venv/bin/activate
pip install -r requirements.txt
```

3. Изменения в конфигурации
   ```bash
   postgres_user -> real value
   postgres_password -> real value
   postgres_database -> real value
   testuser  -> real value
   testpass  -> real value

*alembic.ini*
```ini
sqlalchemy.url = postgresql+asyncpg://postgres_user:postgres_password@db:5432/postgres_database
```


*docker-compose.yml*
```yml
db:
  environment:
    - POSTGRES_USER=postgres_user
    - POSTGRES_PASSWORD=postgres_password
    - POSTGRES_DB=postgres_database

rabbitmq:
  environment:
    - RABBITMQ_DEFAULT_USER=testuser
    - RABBITMQ_DEFAULT_PASS=testpass

```

*config.ini*
```ini
[postgres]
user = postgres_user
pass = postgres_password
   
db = postgresql+asyncpg://postgres_user:postgres_password@db:5432/postgres_database
   
[rabbitmq]
RABBITMQ_URL = amqp://testuser:testpass@rabbitmq/
QUEUE_NAME = order_queue
```

### Сборка и запуск docker-compose

1. Собираем контейнер и запускаем командой:
   ```bash
   docker-compose up -d --build
   ```
   
2. Запускаем миграции:
   ```bash
   docker-compose exec web alembic upgrade head
   ```
   
Теперь это приложение доступно для использования и тестирования по адресу http://localhost:8000.

## Запуск локально без Docker

В этом случае требуется изначально установить локально и запустить [rabbitmq](https://www.rabbitmq.com/docs/download) и [postgres](https://www.enterprisedb.com/downloads/postgres-postgresql-downloads), создать базы

1. Клонируйте репозиторий:

   ```bash
   git clone https://github.com/MrKusaka/testTaskOrders.git
   cd testTaskOrders
    python -m venv venv
    . venv/bin/activate
   pip install -r requirements.txt
   ```

2. В файл alembic.ini заполнить sqlalchemy.url:
   
   ```ini
   sqlalchemy.url = postgresql+asyncpg://postgres_user:postgres_password@localhost:5432/postgres_database

   # postgres_user - Логин от базы данных
   # postgres_password - Пароль от базы данных
   # postgres_database - База данных
   ```

3. В файл config.ini поменять так же на свои данные, логины и пароли:
   
   ```ini
   [postgres]
   user = postgres_user
   pass = postgres_password
   
   db = postgresql+asyncpg://postgres_user:postgres_password@localhost:5432/postgres_database

   [rabbitmq]
   RABBITMQ_URL = amqp://guest:guest@localhost/
   QUEUE_NAME = order_queue
   ```

4. Запустить приложение через терминал командой `uvicorn app.main:app --reload`

5. Запустить тесты через терминал командой `pytest -s -v`
