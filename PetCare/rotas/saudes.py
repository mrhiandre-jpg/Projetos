from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional

#importamos a tabela de pets do arquivo pet.py para poder associar as vacinas e consultas aos pets
from rotas.pet import tabela_de_pets

router = APIRouter()


#Vacinas

class Vacina(BaseModel):
    nome: str
    data_aplicacao: str
    proxima_aplicacao: Optional[str] = None

@router.post("/pets/{pet_id}/vacinas", status_code=201)
def adicionar_vacina(pet_id: int, vacina: Vacina):
    #verifica se o pet existe na tabela
    if pet_id in tabela_de_pets:
        #Transforma os dados da vacina em um dicionário
        nova_vacina = vacina.model_dump()
        nova_vacina["id"] = len(tabela_de_pets[pet_id].get("vacinas", [])) + 1 #Gerando o Id da vacina de uma forma simples

        #Adiciona a vacina ao pet
        if "vacinas" not in tabela_de_pets[pet_id]:
            tabela_de_pets[pet_id]["vacinas"] = []
        tabela_de_pets[pet_id]["vacinas"].append(nova_vacina)

        #retorna a vacina adicionada
        return {
            "mensagem": "Vacina adicionada com sucesso",
            "vacina": nova_vacina
        }
    return {
        "mensagem": "Pet não encontrado"

    }
@router.get("/pets/{pet_id}/vacinas", status_code=200)
def listar_vacinas(pet_id: int):
    #verifica se o pet existe na tabela
    if pet_id in tabela_de_pets:
        #Capturamos o nome do pet para exibir na resposta
        nome_pet = tabela_de_pets[pet_id]["nome"]

        #retorna a lista de vacinas do pet
        return {
            "mensagem": f"lista de vacinas do pet {nome_pet}",
            "vacinas": tabela_de_pets[pet_id].get("vacinas", [])
        }
    return {
        "mensagem": "pet não encontrado"
    }

#consultas

class Consulta(BaseModel):
    data: str
    motivo: str
    veterinario: str
    descricao: Optional[str] = None

@router.post("/pets/{pet_id}/consultas", status_code=201)
def adicionar_consulta(pet_id: int, consulta: Consulta):
    #Verifica se o pet existe na tabela
    if pet_id in tabela_de_pets:
        #Transforma os dados da consulta em um dicionário
        nova_consulta = consulta.model_dump()
        nova_consulta["id"] = len(tabela_de_pets[pet_id].get("consultas", [])) + 1 #Gerando o Id da consulta

        #Adicionando a consulta ao pet
        if "consultas" not in tabela_de_pets[pet_id]:
            tabela_de_pets[pet_id]["consultas"] = []
        tabela_de_pets[pet_id]["consultas"].append(nova_consulta)

        #retorna a consulta adicionada
        return {
            "mensagem": "Consulta adicionada com sucesso",
            "consulta": nova_consulta
        }
    return {
        "mensagem": "Pet não encontrado"
    }

@router.get("/pets/{pet_id}/consultas", status_code=200)
def listar_consultas(pet_id: int):
    #Verifica se o pet existe na tabela
    if pet_id in tabela_de_pets:
        #1 Capturamos o nome do pet para exibir na resposta
        nome_pet = tabela_de_pets[pet_id]["nome"]

        #Retorna a lista de consultas do pet
        return {
            "mensagem": f"lista de consultas do pet {nome_pet}",
            "consultas": tabela_de_pets[pet_id].get("consultas", [])
        }
    return {
        "mensagem": "Pet não encontrado"
    }
