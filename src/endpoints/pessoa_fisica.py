from fastapi import APIRouter, FastAPI
from pymongo import AsyncMongoClient
import models

pf_router = APIRouter(prefix="/perfil_pf", tags=["Perfil Pessoa Física"])

def set_app(app: FastAPI):
    pf_router.context_app = app

pf_router.set_app = set_app

@pf_router.get("/permissao/")
async def listar_permissoes():
    app: FastAPI = pf_router.context_app
    db: AsyncMongoClient = app.state.db
    
    data = db.get_database("lgpd_db")
    res = await data.list_collections()
    res = await res.to_list(length=100)
    print(f"DB State: {res}")
    return [models.Permissao()]

@pf_router.get("/permissao/{id_permissao}")
async def listar_permissao(id_permissao:str):
    return models.Permissao()

@pf_router.post("/permissao/")
async def aprovar_permissao(id_pessoa:str, permissao: models.Permissao):
    print(f"Aprovando permissao para pessoa {id_pessoa}")
    return permissao
