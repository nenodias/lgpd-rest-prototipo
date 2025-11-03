from fastapi import FastAPI
import models


app = FastAPI()


@app.post("/pessoa_fisica/")
async def criar_pessoa(pessoa: models.PessoaFisica):
    return pessoa

@app.post("/pessoa_juridica/")
async def criar_pessoa_juridica(pessoa: models.PessoaJuridica):
    return pessoa

@app.post("/login/")
async def login(login: str, senha: str):
    # Implement login logic here
    return {"message": "Login successful"}


@app.post("/perfil_pj/permissao/")
async def criar_permissao(id_pessoa:str, permissao: models.Permissao):
    print(f"Criando permissao para pessoa {id_pessoa}")
    return permissao

@app.get("/perfil_pj/pessoa_fisica")
async def listar_pessoas_fisicas():
    return [models.PessoaFisica()]

@app.get("/perfil_pj/pessoa_fisica/{id_pessoa}")
async def listar_pessoa_fisica(id_pessoa:str):
    return models.PessoaFisica()



@app.get("/perfil_pf/permissao/")
async def listar_permissoes():
    return [models.Permissao()]

@app.get("/perfil_pf/permissao/{id_permissao}")
async def listar_permissao(id_permissao:str):
    return models.Permissao()

@app.post("/perfil_pf/permissao/")
async def aprovar_permissao(id_pessoa:str, permissao: models.Permissao):
    print(f"Aprovando permissao para pessoa {id_pessoa}")
    return permissao

