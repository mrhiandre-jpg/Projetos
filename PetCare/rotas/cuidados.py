from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional

from rotas.pet import tabela_de_pets

router = APIRouter()

class Banhos(BaseModel):
    data: str
    local: str
    proxima_data: Optional[str] = None

@router.post("/pets/{pet_id}/banhos", status_code=201)
def adicionar_banho(pet_id: int, banho: Banhos):
    #Verifica se o pet existe na tabela
    if pet_id in tabela_de_pets:
        #Transforma os dados do banho em um dicionário
        novo_banho = banho.model_dump()
        novo_banho["id"] = len(tabela_de_pets[pet_id].get("banhos", [])) + 1
        #Adicionando o banho ao pet
        if "banhos" not in tabela_de_pets[pet_id]:
            tabela_de_pets[pet_id]["banhos"] = []
        tabela_de_pets[pet_id]["banhos"].append(novo_banho)

        #retorna o banho adicionado
        return {
            "mensagem": "Banho adicionado com sucesso",
            "banho": novo_banho
        }
    return {
        "mensagem": "Pet não encontrado"
    }

@router.get("/pets/{pet_id}/banhos", status_code=200)
def listar_banhos(pet_id: int):
    #Verifica se o pet existe na tabela
    if pet_id in tabela_de_pets:
        #Capturamos o nome do pet para exibir na resposta
        nome_pet = tabela_de_pets[pet_id]["nome"]

        #Retorna a lista de banhos do pet
        return {
            "mensagem": f"lista de banhos do pet {nome_pet}",
            "banhos": tabela_de_pets[pet_id].get("banhos", [])
        }
    return {
        "mensagem": "Pet não encontrado"
    }

class Alimentacao(BaseModel):
    data: str
    tipo: str
    quantidade: str
    concluido: bool
    observacoes: Optional[str] = None

@router.post("/pets/{pet_id}/alimentacao", status_code=201)
def adicionar_alimentacao(pet_id: int, alimentacao: Alimentacao):
    #Verifica se o pet existe na tabela
    if pet_id in tabela_de_pets:
        #Transforma os dados da alimentação em um dicionário
        nova_alimentacao = alimentacao.model_dump()
        nova_alimentacao["id"] = len(tabela_de_pets[pet_id].get("alimentacao", [])) + 1

        #Adicionando a alimentação ao pet
        if "alimentacao" not in tabela_de_pets[pet_id]:
            tabela_de_pets[pet_id]["alimentacao"] = []
        tabela_de_pets[pet_id]["alimentacao"].append(nova_alimentacao)

        #retorna a alimentação adicionada
        return {
            "mensagem": "Alimentação adicionada com sucesso",
            "alimentacao": nova_alimentacao
        }
    return {
        "mensagem": "Pet não encontrado"
    }

@router.get("/pets/{pet_id}/alimentacao", status_code=200)
def listar_alimentacao(pet_id: int):
    #Verifica se o pet existe na tabela
    if pet_id in tabela_de_pets:
        #Capturamos o nome do pet para exibir na resposta
        nome_pet = tabela_de_pets[pet_id]["nome"]

        #Retorna a lista de alimentação do pet
        return {
            "mensagem": f"lista de alimentação do pet {nome_pet}",
            "alimentacao": tabela_de_pets[pet_id].get("alimentacao", [])
        }
    return {
        "mensagem": "Pet não encontrado"
    }

class Passeio(BaseModel):
    data: str
    local: str
    duracao: str
    observacoes: Optional[str] = None

@router.post("/pets/{pet_id}/passeios", status_code=201)
def adicionar_passeio(pet_id: int, passeio: Passeio):
    #Verifica se o pet existe na tabela
    if pet_id in tabela_de_pets:
        #Transforma os dados do passeio em um dicionário
        novo_passeio = passeio.model_dump()
        novo_passeio["id"] = len(tabela_de_pets[pet_id].get("passeios", [])) + 1

        #Adicionando o passeio ao pet
        if "passeios" not in tabela_de_pets[pet_id]:
            tabela_de_pets[pet_id]["passeios"] = []
        tabela_de_pets[pet_id]["passeios"].append(novo_passeio)

        #retorna o passeio adicionado
        return {
            "mensagem": "Passeio adicionado com sucesso",
            "passeio": novo_passeio
        }
    return {
        "mensagem": "Pet não encontrado"
    }

@router.get("/pets/{pet_id}/passeios", status_code=200)
def listar_passeios(pet_id: int):
    #Verifica se o pet existe na tabela
    if pet_id in tabela_de_pets:
        #Capturamos o nome do pet para exibir na resposta
        nome_pet = tabela_de_pets[pet_id]["nome"]

        #Retorna a lista de passeios do pet
        return {
            "mensagem": f"lista de passeios do pet {nome_pet}",
            "passeios": tabela_de_pets[pet_id].get("passeios", [])
        }
    return {
        "mensagem": "Pet não encontrado"
    }
