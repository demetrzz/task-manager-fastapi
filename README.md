Install

```bash
pip install -e .
```

Configure env:
```bash
export DB_URI=postgresql://postgres:password@localhost
export SECRET_KEY=your_key
export ALGORITHM=your_algorithm
export ACCESS_TOKEN_EXPIRE_MINUTES=minutes
```
Apply migrations
```bash
alembic upgrade head
```
Run

```bash
uvicorn --factory --reload app.main:create_app
```
