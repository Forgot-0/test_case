# FastAPI Participants Management Application

## Описание

Это приложение на основе FastAPI предназначено для управления участниками, включая регистрацию, оценивание и получение списка участников с возможностью фильтрации и сортировки. Приложение использует PostgreSQL с расширением PostGIS для работы с геоданными, Redis для кэширования и отправку электронных писем для уведомлений.

### Предпосылки

- Python 3.8 или выше
- PostgreSQL с установленным расширением PostGIS
- Redis
- Docker


### Configuration
```bash
SECRET=

API_PORT=8000
PYTHONPATH=app
ALGORITHM='HS256'
WATERMAKR_PATH='./VPN_LOGO.jpg'

POSTGRES_DB=
POSTGRES_USER=
POSTGRES_PASSWORD=
POSTGRES_HOST=
POSTGRES_PORT=

REDIS_HOST=redis
REDIS_PORT=6379

EMAIL_USERNAME=
EMAIL_PASSWORD=
EMAIL_FROM=
EMAIL_PORT=587
EMAIL_SERVER=smtp.gmail.com
```
### MakeFile Command
- Создание новой миграции:
```bash
make makemigrations m="Описание миграции"
```
- Миграция базы данных:
```bash
make migrate
```
- Запуск приложения:
```bash
make app_up
```

- Остановка приложения:
```bash
make app_down
```
