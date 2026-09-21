
from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional
from bd.BD import SessionLocal
import bd.model as model


#criei para poder modularizar o código e não deixar tudo no main.py

router = APIRouter()

#Criando o modelo de dados para o usuário
class Usuarios(BaseModel):
    nome: str
    email: str
    senha: str

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

#fazemos a rota para criar um usuário
@router.post("/usuarios", status_code=201)
def criar_usuario(usuario: Usuarios, db: Session = Depends(get_db)):

    novo_usuario = model.UsuarioBD(
        nome=usuario.nome,
        email=usuario.email,
        senha=usuario.senha
    )
@router.get("/usuarios", status_code=200)
def Listar_usuarios():
    #retorna a lista de usuários cadastrados
    return {
        "messagem": "lista de usuários cadastrados",
        "usuarios": tabela_de_usuarios
    }

@router.put("/usuarios/{usuario_id}", status_code=200)
def atualizar_usuario(usuario_id: int, usuario: Usuarios):
    #verifica se o usuário existe na tabela
    if usuario_id in tabela_de_usuarios:

        #Transforma o objeto do usuário em um dicionário
        novo_usuario = usuario.model_dump()
        novo_usuario["id"] = usuario_id
       
        #Substiuindo o usuário antigo pelo novo
        tabela_de_usuarios[usuario_id] = novo_usuario

        #retorna o usuário atualizado
        return {
            "mensagem": "Usuário atualizado com sucesso",
            "usuario": novo_usuario
        }
    return {
        "mensagem": "Usuário não encontrado"
    }


@router.delete("/usuarios/{usuario_id}", status_code=200)
def deletar_usuario(usuario_id: int):
    #Verifica se o usuário existe na tabela
    if usuario_id in tabela_de_usuarios:
        #Deleta o usuário da tabela
        del tabela_de_usuarios[usuario_id]

        return {
            "mensagem": "Usuário deletado com sucesso"
        }
    return {
        "mensagem": "Usuário não encontrado"
    }

#Estoque

class Racao(BaseModel):
    marca: str #Nome da marca da ração
    tipo: str #se e seco, úmido, natural, etc
    para: str #para qual tipo de animal é a ração
    quantidade: float #quantidade de ração em estoque


class Higiene(BaseModel):
    nome: str #Nome do produto de higiene
    tipo: str #se é shampoo, sabonete, etc
    para: str #para qual tipo de animal é o produto
    quantidade: float #quantidade do produto em estoque

class Estoque(BaseModel):
    racao: Optional[list[Racao]] = [] #lista de rações em estoque
    higiene: Optional[list[Higiene]] = [] #lista de produtos de higiene em estoque

@router.put("/usuarios/{usuario_id}/estoque", status_code=200)
def atualizar_estoque(usuario_id: int, estoque: Estoque):
    #verifica se o usuário existe na tabela
    if usuario_id in tabela_de_usuarios:
        #
        tabela_de_usuarios[usuario_id]["estoque"] = estoque.model_dump()

        #retorna o estoque atualizado
        return {
            "mensagem": "Estoque atualizado com sucesso",
            "estoque": tabela_de_usuarios[usuario_id]["estoque"]
        }
    return {
        "mensagem": "Usuário não encontrado"
    }

@router.get("/usuarios/{usuario_id}/estoque", status_code=200)
def listar_estoque(usuario_id: int):
    #verifica se o usuário existe na tabela
    if usuario_id in tabela_de_usuarios:

        estoque_atual = tabela_de_usuarios[usuario_id].get("estoque", {"racao": [], "higiene": []})
    
        #retorna o estoque do usuário
        return {
            "mensagem": "Estoque do usuário",
            "estoque": estoque_atual
        }
    return {
        "mensagem": "Usuário não encontrado"
    }