"""
Módulo de 
"""


from sqlalchemy import Column, Integer, String, Date, ForeignKey, Float, Boolean, DateTime
from sqlalchemy.orm import relationship
from bd.BD import base # Importamos a variável "base"
from datetime import date


# Criando    a tabela real de Usuários no banco de dados
class UsuarioBD(base):
    __tablename__ = "usuarios" # Este será o nome oficial da tabela no banco de dados

    # Definindo as colunas da tabela
    id = Column(Integer, primary_key=True)
    nome = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    senha = Column(String, nullable=False)
    pets = relationship("PetsBD", back_populates="dono")

class EstoqueBD(base):
    __tablename__ = "estoque"

    id = Column(Integer, primary_key=True)
    

    categoria = Column(String, nullable=False) 
    
    # Informações gerais do produto
    nome_produto = Column(String, nullable=False) 
    tipo_produto = Column(String, nullable=False)         
    para = Column(String, nullable=False)        
    
    
    quantidade = Column(Float, nullable=False)    

    usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)









class PetsBD(base):
    __tablename__ = "pets"
    id = Column(Integer, primary_key=True)
    nome = Column(String, nullable=False)
    especie = Column(String, nullable=False)
    data_de_nascimento = Column(Date, nullable=False)
    raca = Column(String, nullable=False)

    usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    dono = relationship("UsuarioBD", back_populates="pets")

    @property
    def idade(self) -> int:
        #Calcula a idade do pet com base na data de nascimento
        hoje = date.today()
        return hoje.year - self.data_de_nascimento.year - (
            (hoje.month, hoje.day) < (self.data_de_nascimento.month, self.data_de_nascimento.day)
        )

class VacinaBD(base):
    __tablename__ = "vacinas"
    id = Column(Integer, primary_key=True)
    nome_vacina = Column(String, nullable=False)
    data_aplicacao = Column(Date, nullable=False)
    proxima_aplicacao = Column(Date, nullable=False)
    pet_id = Column(Integer, ForeignKey("pets.id"), nullable=False)



class FarmaciaBD(base):
    __tablename__ = "farmacia"

    id = Column(Integer, primary_key=True)
    tipo_medicamento = Column(String, nullable=False)
    nome_medicamento = Column(String, nullable=False)
    descricao = Column(String)

    pet_id = Column(Integer, ForeignKey("pets.id"), nullable=False)

class ConsultaBD(base):
    __tablename__ = "consultas"

    id = Column(Integer, primary_key=True)
    data_consulta = Column(DateTime, nullable=False)
    proxima_consulta = Column(DateTime, nullable=True)
    motivo = Column(String, nullable=False)
    descricao = Column(String, nullable=True)
    pet_id = Column(Integer, ForeignKey("pets.id"), nullable=False)


#Cuidados

class BanhoBD(base):
    __tablename__ = "banhos"

    id = Column(Integer, primary_key=True)
    data_banho = Column(Date, nullable=False)
    proxima_data = Column(Date, nullable=True)
    local = Column(String, nullable=False)
    pet_id = Column(Integer, ForeignKey("pets.id"), nullable=False)

class AlimentacaoBD(base):
    __tablename__ = "alimentacao"

    id = Column(Integer, primary_key=True)
    data_alimentacao = Column(DateTime, nullable=False)
    tipo_alimento = Column(String, nullable=False)
    quantidade = Column(String, nullable=False)
    concluido = Column(Boolean, nullable=False)
    observacoes = Column(String, nullable=True)
    pet_id = Column(Integer, ForeignKey("pets.id"), nullable=False)

class PasseioBD(base):
    __tablename__ = "passeios"

    id = Column(Integer, primary_key=True)
    data_passeio = Column(DateTime, nullable=False)
    local = Column(String, nullable=False)
    duracao = Column(String, nullable=False)
    observacoes = Column(String, nullable=True)
    pet_id = Column(Integer, ForeignKey("pets.id"), nullable=False)
