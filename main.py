from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional

# Instância da API
app = FastAPI(title="PetCare Tracker API")

# Banco de dados de usuarios para testar

banco_de_usuarios = []

# Modelo de dados que o usuário vai enviar
class Usuario(BaseModel):
    nome: str
    email: str
    senha: str

# Rota para criar usuário (POST)
@app.post("/usuarios", status_code=201)
def criar_usario(usuario: Usuario):
    #Simulando a criação de um ID no banco de dados
    novo_usuario = usuario.model_dump()
    novo_usuario["id"] = len(banco_de_usuarios) + 1

    #salvando no "BD"
    banco_de_usuarios.append(novo_usuario)

    #retornando o que foi salvo (escondendo a senha por segurança)
    return { 
        "mensagem": "Conta criada com sucesso",
        "usuario": {
            "id": novo_usuario["id"],
            "nome": novo_usuario["nome"],
            "email": novo_usuario["email"]
        }
    }

@app.get("/usuarios", status_code=200)
def listar_usuario():
    # Retorna a lista completa de usuarios
    return {
        "mensagem": "Lista de Usuários recuperada com sucesso",
        "Usuários": banco_de_usuarios
    }

#banco de dados de PETs
banco_de_pets = []

# Modelo de dados que o pet vai enviar
class Pet(BaseModel):
    nome: str
    especie: str
    raca: str
    idade: int

#Rota para criar pet(POST)
@app.post("/pets", status_code=201)
def criar_pets(pet: Pet):
    #Simulando a criação de um ID BD
    novo_pet = pet.model_dump()
    novo_pet["id"] = len(banco_de_pets) + 1

    #salvando BD
    banco_de_pets.append(novo_pet)

    #retornando o que foi salvo
    return {
        "mensagem": "Pet, criado com sucesso",
        "Pet": {
            "id": novo_pet["id"],
            "nome": novo_pet["nome"],
            "especie": novo_pet["especie"],
            "raça": novo_pet["raca"],
            "idade": novo_pet["idade"]
        }
    }
@app.get("/pets", status_code=200)
def listar_pets():
    # Retorna a lista completa de pets que está salva
    return {
        "mensagem": "Lista de pets recuperada com sucesso",
        "pets": banco_de_pets
    }