from bson.objectid import ObjectId as BsonObjectId
from fastapi import APIRouter, FastAPI
from fastapi.responses import JSONResponse
from pymongo.asynchronous.database import AsyncDatabase
import models

pf_router = APIRouter(prefix="/perfil_pf", tags=["Perfil Pessoa Física"])

def set_app(app: FastAPI):
    pf_router.context_app = app

pf_router.set_app = set_app

@pf_router.get("/permissao/", response_model=list[models.Permissao])
async def listar_permissoes(limit: int = 10, skip: int = 0) -> list[models.Permissao]:
    app: FastAPI = pf_router.context_app
    db: AsyncDatabase = app.state.db
    try:
        res = await db["permissoes"].find().skip(skip).limit(limit).to_list(length=limit)
        if not res:
            return []
        else:
            return [models.Permissao(**item) for item in res]
    except Exception as e:
        return []

@pf_router.get("/permissao/{id_permissao}", response_model=models.Permissao | None)
async def listar_permissao(id_permissao:str) -> models.Permissao | None:
    app: FastAPI = pf_router.context_app
    db: AsyncDatabase = app.state.db
    try:
        res = await db["permissoes"].find_one({"_id":BsonObjectId(id_permissao)})
        if not res:
            return None
        else:
            return models.Permissao(**res)
    except Exception as e:
        return None

@pf_router.post("/permissao/", response_model=models.Permissao)
async def aprovar_permissao(id:str) -> models.Permissao:
    app: FastAPI = pf_router.context_app
    db: AsyncDatabase = app.state.db
    try:
        bid = BsonObjectId(id)
        # TODO: Validar se usuario logado tem permissao para aprovar
        res = await db["permissoes"].find_one({"_id":bid})
        if not res:
            return JSONResponse({"message": "Error approving permission"}, status_code=400)
        else:
            db["permissoes"].update_one({"_id":bid}, {"$set":{"aprovada":True}})
            res = await db["permissoes"].find_one({"_id":bid})
            return models.Permissao(**res)
    except Exception as e:
        return JSONResponse({"message": "Error approving permission"}, status_code=500)

