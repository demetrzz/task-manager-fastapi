Install

```bash
pip install -e .
```

Configure env:
```bash
export DB_URI=postgresql://postgres:password@localhost
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
