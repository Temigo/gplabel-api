# GP Label API
With FastAPI, SQLAlchemy. For now the database engine is SQLite.

## Install
```
pip3 install -r requirements.txt
```

## Run API
If you are creating the database from scratch, you will need to run `alembic upgrade head` first.
Then you can run the API server with
```
uvicorn main:app --reload
```
You can add `--log-level "debug"` if needed.

The API will be running at http://localhost:8000. You can consult the (autogenerated) API documentation at http://localhost:8000/redoc.

## Things to know
* Database models (SQLAlchemy) live in `sql_app/models.py`.
* API Pydantic schemas (for validation & interface with database) live in `sql_app/schemas.py`.
* Database CRUD methods live in `sql_app/crud.py`.
* API routes are defined in `main.py`.

## Run migrations
If you change the database models in `sql_app/models.py`, you need to commit it to the database with
```
alembic revision --autogenerate -m "Description"
alembic upgrade head
```
