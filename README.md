Install

```bash
pip install -e .
```

Configure env:
```bash
export DB_URI=postgresql://postgres:password@localhost
SECRET_KEY=your_key
ALGORITHM=your_algorithm
```
if windows PS:
```bash
$Env:DB_URI = "postgresql://postgres:password@localhost" 
```
Apply migrations
```bash
alembic upgrade head
```

Run

```bash
uvicorn --factory --reload app.main:create_app
```
