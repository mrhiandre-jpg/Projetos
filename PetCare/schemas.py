"""
Módulo de Schemas (Pydantic) - Contratos de Dados da API.

Este arquivo define os formatos de entrada (Request) e saída (Response) dos dados
que trafegam pela API. 

Responsabilidades deste módulo:
1. Validar tipos e formatos dos dados enviados pelo cliente antes de chegarem ao banco.
2. Filtrar quais dados serão devolvidos nas respostas HTTP (ocultando dados sensíveis, como senhas).
3. Converter objetos do banco de dados (SQLAlchemy Models) em JSON.
"""



from pydantic import BaseModel, ConfigDict, EmailStr
from datetime import date, datetime
from typing import Optional



#---------------------------------------------
#1. Usuarios
#---------------------------------------------

###Usuarios
class UsuarioBase(BaseModel):
    nome: str
    email: EmailStr

class UsuarioCreate(UsuarioBase):
    """Recebe os dados no cadastro (inclui a senha)."""
    senha: str

class UsuarioResponse(UsuarioBase):
    """Devolve os dados na API, sem a senha."""
    id: int
    model_config = ConfigDict(from_attributes=True)

#---------------------------------------------
#2. Estoque
#---------------------------------------------

class EstoqueCreate(BaseModel):
    categoria: str
    nome_produto: str
    tipo_produto: str
    para: str
    quantidade: float
    usuario_id: int


#---------------------------------------------
#3. Pets
#---------------------------------------------


class PetCreate(BaseModel):
    nome: str
    especie: str
    data_de_nascimento: date
    raca: str
    usuario_id: int 

class PetResponse(PetCreate):
    id: int
    idade: int
    model_config = ConfigDict(from_attributes=True)


#---------------------------------------------
# 4. SAÚDE DO PET
#---------------------------------------------

class VacinaCreate(BaseModel):
    nome_vacina: str
    data_aplicacao: date
    proxima_aplicacao: Optional[date] = None
    pet_id: int

class ConsultaCreate(BaseModel):
    data_consulta: datetime  # Data e hora da consulta
    motivo: str
    descricao: Optional[str] = None
    proxina_consulta: Optional[datetime] = None
    pet_id: int


#---------------------------------------------
# 5. CUIDADOS E ROTINA DO PET
#---------------------------------------------

class BanhoCreate(BaseModel):
    data_banho: date
    local: str
    proxima_data: Optional[date] = None
    pet_id: int

class AlimentacaoCreate(BaseModel):
    data_alimentacao: datetime
    tipo_alimento: str
    quantidade: str
    concluido: bool = False
    observacoes: Optional[str] = None
    pet_id: int

class PasseioCreate(BaseModel):
    data_passeio: datetime
    local: str
    duracao: str
    observacoes: Optional[str] = None
    pet_id: int