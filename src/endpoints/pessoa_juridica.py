from bson.objectid import ObjectId as BsonObjectId
from typing import List
from fastapi import APIRouter, FastAPI, Request
from fastapi.responses import JSONResponse
from pymongo.asynchronous.database import AsyncDatabase
import models

pj_router = APIRouter(prefix="/perfil_pj", tags=["Perfil Pessoa Jurídica"])

def set_app(app: FastAPI):
    pj_router.context_app = app

pj_router.set_app = set_app

@pj_router.post("/permissao/", response_model=models.Permissao)
async def criar_permissao(permissao: models.Permissao, request: Request) -> models.Permissao:
    app: FastAPI = pj_router.context_app
    db: AsyncDatabase = app.state.db
    identity = request.scope.get("current_user")["_id"]
    try:
        permissao.id_pessoa_juridica = identity
        permissao.aprovada = False
        res = await db["permissoes"].find_one({"id_pessoa_juridica":identity,"id_pessoa":permissao.id_pessoa})
        if res:
            permissao.id = res["_id"]
            db["permissoes"].update_one({"_id":permissao.id}, {"$set":permissao.model_dump(exclude={"id"})})
            res = await db["permissoes"].find_one({"_id":permissao.id})
            return models.Permissao(**res)
        res = await db["permissoes"].insert_one(permissao.model_dump(exclude={"id"}))
        res = await db["permissoes"].find_one({"_id":res.inserted_id})
        return models.Permissao(**res)
    except Exception as e:
        print(e)
        return JSONResponse({"message": "Error creating permission"}, status_code=500)

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
        print(e)
        return []

@pj_router.get("/pessoa_fisica/{id_pessoa}", response_model=models.PessoaFisica | None)
async def listar_pessoa_fisica(id_pessoa:str, request: Request) -> models.PessoaFisica | None:
    app: FastAPI = pj_router.context_app
    db: AsyncDatabase = app.state.db
    identity = request.scope.get("current_user")["_id"]
    bid = BsonObjectId(id_pessoa)
    try:
        res = await db["pessoas_fisicas"].find_one({"_id":bid})
        permissao = await db["permissoes"].find_one({"id_pessoa_juridica":identity,"id_pessoa":bid,"aprovada":True})
        if not permissao:
            return None
        else:
            res = models.PessoaFisica(**res)
            if permissao["dados_basicos"] == False:
                res.basicos.name = "**********"
                res.basicos.email = "**********"
                res.basicos.login = "**********"
            if permissao["dados_sensiveis"] == False:
                res.informacoes_sensiveis.cpf = "**********"
                res.informacoes_sensiveis.rg = "**********"
            if permissao["comunicacao"] == False:
                res.comunicacao = None
            if permissao["localizacao"] == False:
                res.localizacao = None
            return res
    except Exception as e:
        print(e)
        return []
