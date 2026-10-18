from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import Relationship
from bd.BD import base # Importamos a variável "base"
from datetime import date


# Criando a tabela real de Usuários no banco de dados
class UsuarioBD(base):
    __tablename__ = "usuarios" # Este será o nome oficial da tabela no banco de dados

    # Definindo as colunas da tabela
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    senha = Column(String, nullable=False)
    pets = Relationship("PetsBD", back_populates="dono")

class PetsBD(base):
    __tablename__ = "pets"
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    especie = Column(String, nullable=False)
    idade_pet = Column(Date, nullable=False)
    raca = Column(String, nullable=False)

    usuario_id = Column(Integer, ForeignKey("usuarios.id"))
    dono = Relationship("UsuarioBD", back_populates="pets")

    @property
    def idade(self) -> int:
        hoje = date.today()
        return hoje.year - self.idade_pet.year - (
            (hoje.month, hoje.day) < (self.idade_pet.month, self.idade_pet.day)
        )

class SaudesBD(base):
    __tablename__ = "saude"
    id = Column(Integer, primary_key=True, index=True)
    nome_vacina = Column(String, nullable=False)
    data_aplicacao = Column(Date, nullable=False)
    proxima_aplicacao = Column(Date, nullable=False)

