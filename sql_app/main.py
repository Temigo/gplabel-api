from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from . import crud, models, schemas
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        # See https://github.com/sqlalchemy/sqlalchemy/discussions/9167
        # and https://github.com/sqlalchemy/sqlalchemy/discussions/9188
        engine.dispose()
