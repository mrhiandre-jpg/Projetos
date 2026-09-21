from fastapi import FastAPI
from rotas import usuario, pet, saudes, cuidados #importamos o arquivo rotas
from bd.BD import engine #importamos o arquivo model
from bd import model


#A função principal do FastAPI é criar a aplicação
app = FastAPI(title="PetCare", description="API para gerenciamento de usuários e estoque de produtos para pets", version="1.0.0")

#conectamos o módulo da rota usuário

app.include_router(usuario.router)

#conectamos o módulo da rota pet
app.include_router(pet.router)
app.include_router(saudes.router)
app.include_router(cuidados.router)



# Database

#criando o banco de dados
model.base.metadata.create_all(bind=engine)
