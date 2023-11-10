# TaskManager

## API для приложения - менеджмента задач

### Стек технологий:
- Python
- FastAPI
- SQLAlchemy
- PostgreSQL
- Alembic
- Pydantic
- Pytest
### Установка и настройка:

```bash
pip install -e .
```

### Настроить env:
```bash
export DB_URI=postgresql://postgres:password@localhost
export SECRET_KEY=your_key
export ALGORITHM=your_algorithm
export ACCESS_TOKEN_EXPIRE_MINUTES=minutes
```
### Применить миграции
```bash
alembic upgrade head
```
### Запустить:

```bash
uvicorn --factory --reload app.main:create_app
```
