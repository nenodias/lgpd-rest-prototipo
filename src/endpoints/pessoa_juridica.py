from bson.objectid import ObjectId as BsonObjectId
from typing import List
from fastapi import APIRouter, FastAPI
from fastapi.responses import JSONResponse
from pymongo.asynchronous.database import AsyncDatabase
import models

pj_router = APIRouter(prefix="/perfil_pj", tags=["Perfil Pessoa Jurídica"])

def set_app(app: FastAPI):
    pj_router.context_app = app

pj_router.set_app = set_app

@pj_router.post("/permissao/", response_model=models.Permissao)
async def criar_permissao(id_pessoa:str, permissao: models.Permissao) -> models.Permissao:
    print(f"Criando permissao para pessoa {id_pessoa}")
    return permissao

@pj_router.get("/pessoa_fisica", response_model=List[models.PessoaFisicaListagem])
async def listar_pessoas_fisicas(limit: int = 10, skip: int = 0) -> list[models.PessoaFisicaListagem]:
    app: FastAPI = pj_router.context_app
    db: AsyncDatabase = app.state.db
    try:
        res = await db["pessoas_fisicas"].find().skip(skip).limit(limit).to_list(length=limit)
        if not res:
            return []
        else:
            return [models.PessoaFisicaListagem(**item) for item in res]
    except Exception as e:
        return []

@pj_router.get("/pessoa_fisica/{id_pessoa}", response_model=models.PessoaFisica | None, response_model_exclude={"senha", "confirmacao_senha"})
async def listar_pessoa_fisica(id_pessoa:str) -> models.PessoaFisica | None:
    return models.PessoaFisica()
