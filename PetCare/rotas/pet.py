from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional

router = APIRouter ()
#utilizamos um dicionario para simular uma tabela de dados de pets
tabela_de_pets = {}

#criando o modelo de dados para o pet
class Pets(BaseModel):
    nome: str
    especie: str
    idade: Optional[int] = None
    raca: str

@router.post("/pets", status_code=201)
def criar_pet(pet: Pets):
    novo_pet = pet.model_dump()
    novo_pet["id"] = len(tabela_de_pets) + 1 #Gerando o Id do pet de uma forma simples

    #salndo na "tabela" de pets (simulado aqui com uma lista)
    tabela_de_pets[novo_pet["id"]] = novo_pet

    #retorna o pet criado
    return {
        "mensagem": "Pet criado com sucesso",
        "pet": {
            "id": novo_pet["id"],
            "nome": novo_pet["nome"],
            "especie": novo_pet["especie"],
            "idade": novo_pet["idade"],
            "raca": novo_pet["raca"]
        }
    }

@router.get("/pets", status_code=200)
def listar_pets():
    #retona a lista dos pets cadastrados
    return {
        "mensagem": "lista de pets cadastrados",
        "pets": tabela_de_pets
    }
@router.put("/pets/{pet_id}", status_code=200)
def atualizar_pet(pet_id: int, pet: Pets):
    #verifica se o pet existe na tabela
    if pet_id in tabela_de_pets:
        #Transforma os dados do pet em um dicionário
        novo_pet = pet.model_dump()
        novo_pet["id"] = pet_id

        #Substitui o pet antigo pelo novo
        tabela_de_pets[pet_id] = novo_pet

        #retorna o pet atualizado
        return {
            "mensagem": "Pet atualizado com sucesso",
            "pet": novo_pet
        }
    return {
        "mensagem": "Pet não encontrado"
    }
@router.delete("/pets/{pet_id}", status_code=200)
def deletar_pet(pet_id: int):
    #verifica se o pet existe na tabela
    if pet_id in tabela_de_pets:
        #remove o pet da tabela
        del tabela_de_pets[pet_id]

        #retorna a mensagem de sucesso
        return {
            "mensagem": "Pet deletado com sucesso"
        }