import os, bcrypt, jwt
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from bson.objectid import ObjectId as BsonObjectId
from pymongo.asynchronous.database import AsyncDatabase
from contextlib import asynccontextmanager
from auth import AuthMiddleware

import db
import models
import endpoints

@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.client = await db.get_database()
    app.state.db = app.state.client.get_database(os.getenv("MONGO_INITDB_DATABASE", "lgpd_db"))
    yield
    app.state.db = None
    await db.close_database(app.state.client)

app = FastAPI(
    title="LGPD-REST-PROTOTIPO",
    description="",
    summary="API para gerenciamento de permissões conforme a LGPD",
    version="0.0.1",
    contact={
        "name": "Horácio Dias Baptista Neto",
        "url": "https://linkedin.com/in/nenodias",
        "email": "horacio.dias@yahoo.com",
    },
    license_info={
        "name": "Apache 2.0",
        "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
    },
    lifespan=lifespan,
)

def limpar_senha_e_salt(pessoa) -> models.CriarPessoaFisica | models.CriarPessoaJuridica:
    pessoa.salt = ""
    pessoa.senha = ""
    pessoa.confirmacao_senha = ""
    return pessoa

@app.post("/pessoa_fisica/", response_model=models.CriarPessoaFisica)
async def criar_pessoa(pessoa: models.CriarPessoaFisica):
    if pessoa.senha != pessoa.confirmacao_senha:
        return JSONResponse({"message": "Password confirmation does not match"}, status_code=400)
    salt = bcrypt.gensalt()
    pessoa.salt = salt.decode('utf-8')
    hashed = bcrypt.hashpw(pessoa.senha.encode('utf-8'), salt=salt)
    pessoa.senha = hashed.decode('utf-8')
    pessoa.confirmacao_senha = hashed.decode('utf-8')
    db: AsyncDatabase = app.state.db
    dados = pessoa.model_dump(exclude={"id", "confirmacao_senha"})
    
    res = await db["pessoas_fisicas"].find({"informacoes_sensiveis.cpf": pessoa.informacoes_sensiveis.cpf}).to_list(1)
    if len(res) > 0:
        return JSONResponse({"message": "CPF já cadastrado"}, status_code=400)
    res = await db["pessoas_fisicas"].insert_one(dados)
    res = await db["pessoas_fisicas"].find_one({"_id":res.inserted_id})
    return limpar_senha_e_salt(models.CriarPessoaFisica(**res))

@app.post("/pessoa_juridica/", response_model=models.CriarPessoaJuridica)
async def criar_pessoa_juridica(pessoa: models.CriarPessoaJuridica):
    if pessoa.senha != pessoa.confirmacao_senha:
        return JSONResponse({"message": "Password confirmation does not match"}, status_code=400)
    salt = bcrypt.gensalt()
    pessoa.salt = salt.decode('utf-8')
    hashed = bcrypt.hashpw(pessoa.senha.encode('utf-8'), salt=salt)
    pessoa.senha = hashed.decode('utf-8')
    pessoa.confirmacao_senha = hashed.decode('utf-8')

    db: AsyncDatabase = app.state.db
    res = await db["pessoas_juridicas"].find({"cnpj": pessoa.cnpj}).to_list(1)
    if len(res) > 0:
        return JSONResponse({"message": "CNPJ já cadastrado"}, status_code=400)
    dados = pessoa.model_dump(exclude={"id", "confirmacao_senha"})
    res = await db["pessoas_juridicas"].insert_one(dados)
    res = await db["pessoas_juridicas"].find_one({"_id":res.inserted_id})
    return limpar_senha_e_salt(models.CriarPessoaJuridica(**res))


@app.post("/login-pf/")
async def login(login: str, senha: str):
    db: AsyncDatabase = app.state.db
    try:
        registro = await db["pessoas_fisicas"].find_one({"basicos.login":login})
        if not registro:
            return JSONResponse({"message": "Invalid login or password"}, status_code=401)
        salt = registro["salt"].encode('utf-8')
        hashed = bcrypt.hashpw(senha.encode('utf-8'), salt=salt)
        if hashed.decode('utf-8') != registro["senha"]:
            return JSONResponse({"message": "Invalid login or password"}, status_code=401)  
        encoded_jwt = jwt.encode({"id": str(registro["_id"])}, os.getenv("APP_SECRET_KEY", "secret"), algorithm="HS256")
        return {"message": "Login successful", "token": encoded_jwt}
    except Exception as e:
        print(e)
        return JSONResponse({"message": "Error approving permission"}, status_code=500)


@app.post("/login-pj/")
async def login(login: str, senha: str):
    db: AsyncDatabase = app.state.db
    try:
        registro = await db["pessoas_juridicas"].find_one({"basicos.login":login})
        if not registro:
            return JSONResponse({"message": "Invalid login or password"}, status_code=401)
        salt = registro["salt"].encode('utf-8')
        hashed = bcrypt.hashpw(senha.encode('utf-8'), salt=salt)
        if hashed.decode('utf-8') != registro["senha"]:
            return JSONResponse({"message": "Invalid login or password"}, status_code=401)  
        encoded_jwt = jwt.encode({"id": str(registro["_id"])}, os.getenv("APP_SECRET_KEY", "secret"), algorithm="HS256")
        return {"message": "Login successful", "token": encoded_jwt}
    except Exception as e:
        print(e)
        return JSONResponse({"message": "Error approving permission"}, status_code=500)

app.add_middleware(AuthMiddleware, routes=["/perfil_pj/**", "/perfil_pf/**"], aplicacao=app)

app.include_router(endpoints.pj_router)
app.include_router(endpoints.pf_router)

for router in [endpoints.pj_router, endpoints.pf_router]:
    if hasattr(router, "set_app"):
        router.set_app(app)
