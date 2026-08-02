## Запуск проекта в Docker
1. Создайте файл `.env` на основе `.env.sample` и заполните переменные.
2. Выполните команду для сборки и запуска:
   ```bash
   docker compose up --build
   ```
3. В новом терминале примените миграции:
   ```bash
   docker compose exec web python manage.py migrate
   ```
