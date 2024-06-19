from sqlalchemy import create_engine, event
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.core.env_settings import settings

class Database:
    SCHEMA_NAME = settings.POSTGRES_SCHEMA
    def __init__(self):
        SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.POSTGRES_USER}:{settings.POSTGRES_PASSWORD}@{settings.POSTGRES_HOSTNAME}:{settings.DATABASE_PORT}/{settings.POSTGRES_DB}"
        self.engine = create_engine(SQLALCHEMY_DATABASE_URL)
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
        self.Base = declarative_base()
        
        # Attach the event listener for setting the search path
        event.listen(self.engine, "connect", self.set_search_path)

    def set_search_path(self, dbapi_connection, connection_record):
        cursor = dbapi_connection.cursor()
        cursor.execute(f'SET search_path TO {self.SCHEMA_NAME}')
        cursor.close()
            
    def get_db(self):
        db = self.SessionLocal()
        try:
            yield db
        finally:
            db.close()

database = Database()
Base = database.Base
engine = database.engine
get_db = database.get_db

# Ensure models are imported here
from app.model.user import User