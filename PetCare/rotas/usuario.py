
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from bd.BD import SessionLocal
from bd import model
from schemas import UsuarioCreate, UsuarioResponse 

#criei para poder modularizar o código e não deixar tudo no main.py

router = APIRouter()

#Criando o modelo de dados para o usuário
"""class Usuarios(BaseModel):
    nome: str
    email: str
    senha: str"""

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

#fazemos a rota para criar um usuário
@router.post("/usuarios", status_code=201, response_model=UsuarioResponse)
def criar_usuario(usuario: UsuarioCreate, db: Session = Depends(get_db)):

    novo_usuario = model.UsuarioBD(**usuario.model_dump())
    try:
        db.add(novo_usuario)
        db.commit()
        db.refresh(novo_usuario)
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail=f"Email ja cadastrado")
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Não foi possivel criar o usuario: {e}")

    return novo_usuario
@router.get("/usuarios", status_code=200, response_model=list[UsuarioResponse])
def Listar_usuarios(db: Session = Depends(get_db)):
    #retorna a lista de usuários cadastrados
    return db.query(model.UsuarioBD).all()


@router.put("/usuarios/{usuario_id}", status_code=200, response_model=UsuarioResponse)
def atualizar_usuario(usuario_id: int, usuario: UsuarioCreate, db: Session = Depends(get_db)):
    #verifica se o usuário existe na tabela
    usuario_bd = db.get(model.UsuarioBD, usuario_id)
    if not usuario_bd:
        raise HTTPException(status_code=404, detail=f"Não foi possivel encontrar o usuario")


    usuario_bd.nome = usuario.nome
    usuario_bd.email = usuario.email
    usuario_bd.senha = usuario.senha

    try:
        db.add(usuario_bd)
        db.commit()
        db.refresh(usuario_bd)
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail=f"Email ja cadastrado")
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Não foi possivel atualizar o usuario")
    return usuario_bd

"""
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
    }"""