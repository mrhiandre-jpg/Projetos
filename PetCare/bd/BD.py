from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

#criando o arquivo de banco de dados
SQLALCHEMY_DATABASE_URL = "sqlite:///./bd/petcare.db"

#Criamos a conexão com o banco de dados
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})

#Criamos a sessão do banco de dados
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

base = declarative_base()
