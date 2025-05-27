from sqlalchemy import create_engine, Column, Integer, String, Boolean # permite definir os tipos de dados e colunas das tabelas
from sqlalchemy.ext.declarative import declarative_base # cria uma classe base para definir os modelos do banco
from sqlalchemy.orm import sessionmaker # cria sessões para interações com o banco (crud)

DATABASE_URL = "sqlite:///./notes.bd" # endereço url do banco

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False}) # gerencia a comunicação com o banco
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()   # classe abstratata que será herdada pelas classes do modelo
                            # armazena metadados e o mapeamentto entre as classes py e sql 

# define classe Note que representa uma tabela chamada notes
class Note(Base):
    __tablename__ = "notes"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String)
    image = Column(String, nullable=True) # opcional
    completed = Column(Boolean, default=True)

def create_db():
    Base.metadata.create_all(bind=engine) # lê todos os modelos que herdaram Base e cria o notes.db e gera a tabela notes com as colunas definidas
