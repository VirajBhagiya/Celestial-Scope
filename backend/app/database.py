from sqlalchemy import create_engine, text
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.exc import OperationalError
from .config import settings

SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}'

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def check_and_create_database():
    temp_engine = create_engine(f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}')
    try:
        with temp_engine.connect() as conn:
            # Try to check if the database exists
            result = conn.execute(
                text(f"SELECT 1 FROM pg_database WHERE datname = '{settings.database_name}'")
            ).fetchone()

            if not result:
                print(f"Database {settings.database_name} does not exist. Creating it...")
                conn.execute(text(f"COMMIT"))
                conn.execute(text(f"CREATE DATABASE {settings.database_name}"))
                print(f"Database {settings.database_name} created successfully.")
            else:
                print(f"Database {settings.database_name} already exists.")
    except OperationalError as e:
        print(f"Error connecting to the database server: {e}")
    finally:
        temp_engine.dispose()

def create_tables():
    try:
        Base.metadata.create_all(bind=engine)
        print("Tables created successfully.")
    except Exception as e:
        print(f"Error creating tables: {e}")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
check_and_create_database()
create_tables()