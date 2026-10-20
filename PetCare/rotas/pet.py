from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from bd.BD import SessionLocal
from bd import model
from schemas import PetCreate, PetResponse

router = APIRouter ()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


"""#criando o modelo de dados para o pet
class PetsCreate(BaseModel):
    nome: str
    especie: str
    idade_pet: date
    raca: str
    usuario_id: int """

@router.post("/pets", status_code=201, response_model=PetResponse)
def criar_pet(pet: PetCreate, db: Session = Depends(get_db)):
    dono = db.get(model.UsuarioBD, pet.usuario_id)
    if not dono:
        raise HTTPException(status_code=404, detail=f"Não foi possivel encontrar o dono")   


    novo_pet = model.PetsBD(**pet.model_dump())
    try:
        db.add(novo_pet)
        db.commit()
        db.refresh(novo_pet)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Não foi possível criar o pet: {e}")

    return novo_pet
""" @router.get("/pets", status_code=200)
def listar_pets():
    #retona a lista dos pets cadastrados
    return {
        "mensagem": "lista de pets cadastrados",
        "pets": tabela_de_pets
        
    }
@router.put("/pets/{pet_id}", status_code=200)
def atualizar_pet(pet_id: int, pet: PetsCreate,):
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
        }"""