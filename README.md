# Chats API

Приложение на FastAPI для работы с чатами и сообщениями с использованием PostgreSQL.  
Docker используется для упрощения развёртывания.

1. Клонируем репозиторий
git clone "https://github.com/luckyping666/chats-api"
cd chats

2. Создаем файл .env в корне проекта и указываем путь к БД
touch .env
DATABASE_URL=postgresql+asyncpg://postgres:postgres@db:5432/chat_db

3. Создаем контейнеры
docker compose up --build

4. Применяем миграции
docker compose exec web alembic upgrade head

5. Открываем swagger и тестируем api
http://localhost:8000/docs

6. Для запуска тестов необходимо ввести команду
docker compose exec web pytest src/tests -v
