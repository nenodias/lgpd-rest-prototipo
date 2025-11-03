from fastapi import APIRouter, FastAPI
from contextlib import asynccontextmanager
from auth import AuthMiddleware

import db
import models
import endpoints

@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.db = await db.get_database()
    yield
    await db.close_database(app.state.db)

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


@app.post("/pessoa_fisica/")
async def criar_pessoa(pessoa: models.PessoaFisica):
    return pessoa

@app.post("/pessoa_juridica/")
async def criar_pessoa_juridica(pessoa: models.PessoaJuridica):
    return pessoa

@app.post("/login/")
async def login(login: str, senha: str):
    return {"message": "Login successful"}


app.add_middleware(AuthMiddleware, routes=["/perfil_pj/**", "/perfil_pf/**"])

app.include_router(endpoints.pj_router)
app.include_router(endpoints.pf_router)
for router in [endpoints.pj_router, endpoints.pf_router]:
    if hasattr(router, "set_app"):
        router.set_app(app)
