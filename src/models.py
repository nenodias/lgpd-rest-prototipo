import uuid
from pydantic import BaseModel, Field


class Basicos(BaseModel):
    name: str
    email: str
    login: str

class InformacoesSensiveis(BaseModel):
    cpf: str | None = None
    rg: str | None = None

class Telefone(BaseModel):
    numero: str
    tipo: str

class RedesSociais(BaseModel):
    plataforma: str
    username: str

class Endereco(BaseModel):
    numero: str
    rua: str
    bairro: str
    cidade: str
    estado: str
    cep: str
    pais: str

class Comunicacao(BaseModel):
    telefones: list[Telefone] | None = None
    fax: str | None = None
    redes_sociais: list[RedesSociais] | None = None
    site: str | None = None

class Localizacao(BaseModel):
    enderecos: list[Endereco] | None = None

class PessoaFisica(BaseModel):
    id: uuid.UUID = Field(default_factory=uuid.uuid4)
    basicos: Basicos
    informacoes_sensiveis: InformacoesSensiveis
    comunicacao: Comunicacao | None = None
    localizacao: Localizacao | None = None
    senha: str
    confirmacao_senha: str

class PessoaJuridica(BaseModel):
    id: uuid.UUID = Field(default_factory=uuid.uuid4)

    nome_fantasia: str
    cnpj: str
    inscricao_estadual: str | None = None

    basicos: Basicos
    comunicacao: Comunicacao | None = None
    localizacao: Localizacao | None = None

    senha: str
    confirmacao_senha: str


class Permissao(BaseModel):
    id: uuid.UUID = Field(default_factory=uuid.uuid4)
    id_pessoa: uuid.UUID = Field(default_factory=uuid.uuid4)
    id_pessoa_juridica: uuid.UUID = Field(default_factory=uuid.uuid4)

    dados_basicos: bool = False
    dados_sensiveis: bool = False
    comunicacao: bool = False
    localizacao: bool = False
