from fastapi import FastAPI, HTTPException
from sqlalchemy import create_engine, Column, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Criar uma instância do FastAPI
app = FastAPI()
 

# Criar a conexão com o banco de dados
SQLALCHEMY_DATABASE_URL = "postgresql://username:password@localhost/postgres"
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Criar uma sessão do SQLAlchemy
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Definir o modelo SQLAlchemy
class Item(Base):
    __tablename__ = "items"

    name = Column(String, primary_key=True, index=True)
    description = Column(String, index=True)
    price = Column(Float)
    tax = Column(Float)

# Criar as tabelas no banco de dados
Base.metadata.create_all(bind=engine)

# Definir operações CRUD para o banco de dados
def get_item(db_session, item_name: str):
    return db_session.query(Item).filter(Item.name == item_name).first()

def create_item(db_session, item_data):
    db_item = Item(**item_data)
    db_session.add(db_item)
    db_session.commit()
    db_session.refresh(db_item)
    return db_item

# Rota para criar um novo item
@app.post("/items/")
async def create_item(item: Item):
    db = SessionLocal()
    db_item = create_item(db, item.dict())
    db.close()
    return db_item

# Rota para obter um item pelo nome
@app.get("/items/{item_name}")
async def read_item(item_name: str):
    db = SessionLocal()
    db_item = get_item(db, item_name)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    db.close()
    return db_item

