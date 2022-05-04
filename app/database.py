from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


# SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"
# engine = create_engine(
#     SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
# )
# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

SQLALCHEMY_DATABASE_URL = "postgresql://postgres:postgres@localhost/fast_api_social_db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, future=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine, future=True)

Base = declarative_base()


def get_db():
    try:
        print("Trying to get the db cursor...")
        db = SessionLocal()
        yield db
    except:
        print("Database connection failed...")
    finally:
        print("Closing the connection...")
        db.close()
        print("Closed!")
