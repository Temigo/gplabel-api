from sqlalchemy import create_engine, inspect
from sqlalchemy.ext.declarative import declarative_base, as_declarative
from sqlalchemy.orm import sessionmaker

# This will be used in root `main.py` file, path needs to be relative
# to the root folder.
import os
SQLALCHEMY_DATABASE_URL = os.getenv("SQL_URL", "sqlite:///./sql_app/sql_app.db")
# SQLALCHEMY_DATABASE_URL = "postgresql://user:password@postgresserver/db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

#Base = declarative_base()
@as_declarative()
class Base:
    def _asdict(self):
        return {c.key: getattr(self, c.key)
                for c in inspect(self).mapper.column_attrs}
