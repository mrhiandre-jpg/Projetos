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
    except Exception:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Não foi possível criar o pet")

    return novo_pet
@router.get("/pets", status_code=200, response_model=list[PetResponse])
def listar_pets(db: Session = Depends(get_db)):

    return db.query(model.PetsBD).all()
    #retona a lista dos pets cadastrados

@router.put("/pets/{pet_id}", status_code=200, response_model=PetResponse)
def atualizar_pet(pet_id: int, pet: PetCreate, db: Session = Depends(get_db)):
    #verifica se o pet e o novo dono existe na tabela  
    pet_bd = db.get(model.PetsBD, pet_id)
    if not pet_bd :
        raise HTTPException(status_code=404, detail=f"Não foi possivel encontrar o Pet")

    if not db.get(model.UsuarioBD, pet.usuario_id):
        raise HTTPException(status_code=404, detail=f"Não foi possivel encontrar o Usuario") 

    pet_bd.nome = pet.nome
    pet_bd.especie = pet.especie
    pet_bd.data_de_nascimento = pet.data_de_nascimento
    pet_bd.raca = pet.raca
    pet_bd.usuario_id = pet.usuario_id

    try:
        db.add(pet_bd)
        db.commit()
        db.refresh(pet_bd)
    except Exception:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Não foi possivel atualizar o pet")
    return pet_bd
    
"""
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