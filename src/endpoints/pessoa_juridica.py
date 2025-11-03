from fastapi import APIRouter, FastAPI
import models

pj_router = APIRouter(prefix="/perfil_pj", tags=["Perfil Pessoa Jurídica"])

def set_app(app: FastAPI):
    pj_router.context_app = app

pj_router.set_app = set_app

@pj_router.post("/permissao/")
async def criar_permissao(id_pessoa:str, permissao: models.Permissao):
    print(f"Criando permissao para pessoa {id_pessoa}")
    return permissao

@pj_router.get("/pessoa_fisica")
async def listar_pessoas_fisicas():
    return [models.PessoaFisica()]

@pj_router.get("/pessoa_fisica/{id_pessoa}")
async def listar_pessoa_fisica(id_pessoa:str):
    return models.PessoaFisica()
