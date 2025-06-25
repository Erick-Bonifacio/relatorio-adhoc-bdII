from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# ALTERE PARA ACESSAR O SEU BANCO DE DADOS:
DATABASE_URL = "postgresql://postgres:root@localhost:5433/bd_dois_app"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

def GetDBSession():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()