import uuid
from bson.objectid import ObjectId as BsonObjectId
from pydantic import BaseModel, computed_field
from typing import Any, Optional, List, Dict


class PydanticObjectId(BsonObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v: Any, *args) -> BsonObjectId:
        """
        Validate input for ObjectId fields.
        Accepts:
          - a bson ObjectId -> returns it
          - a valid ObjectId string -> converts and returns ObjectId
        Raises ValueError for invalid values.
        Accepts extra args for compatibility with different pydantic call signatures.
        """
        if isinstance(v, BsonObjectId):
            return v
        if isinstance(v, str):
            if BsonObjectId.is_valid(v):
                return BsonObjectId(v)
            raise ValueError("Invalid ObjectId string")
        raise TypeError("ObjectId required")

    @classmethod
    def __get_pydantic_json_schema__(cls, core_schema, handler) -> Dict[str, Any]:
        """
        Pydantic v2 hook to provide JSON Schema for this custom type.
        Accepts (core_schema, handler). Use handler(core_schema) when available
        to derive a base schema, then adjust to represent ObjectId as string.
        """
        schema: Dict[str, Any]
        try:
            if callable(handler):
                schema = handler(core_schema) or {}
            else:
                schema = {}
        except Exception:
            schema = {}

        # ensure it's represented as a string with uuid-like/objectid format in docs
        schema.update({"type": "string", "format": "objectid", "example": "650b9c8f2f9b5a1b2c3d4e5f"})
        return schema


# Common base model to include json encoders for ObjectId (Pydantic v2)
class LGPDBaseModel(BaseModel):
    
    @computed_field()
    def id(self) -> str:
        if hasattr(self, "_id"):
            return str(self._id)
        else:
            return str(BsonObjectId())
    
    model_config = {
        "arbitrary_types_allowed": True,
        "json_encoders": {BsonObjectId: lambda v: str(v)},
    }


class Basicos(BaseModel):
    name: str
    email: str
    login: str


class InformacoesSensiveis(BaseModel):
    cpf: Optional[str] = None
    rg: Optional[str] = None


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
    telefones: Optional[List[Telefone]] = None
    fax: Optional[str] = None
    redes_sociais: Optional[List[RedesSociais]] = None
    site: Optional[str] = None


class Localizacao(BaseModel):
    enderecos: Optional[List[Endereco]] = None


class PessoaFisicaListagem(LGPDBaseModel):
    basicos: Basicos


class PessoaFisica(LGPDBaseModel):
    basicos: Basicos
    informacoes_sensiveis: InformacoesSensiveis
    comunicacao: Optional[Comunicacao] = None
    localizacao: Optional[Localizacao] = None

class CriarPessoaFisica(LGPDBaseModel):
    basicos: Basicos
    informacoes_sensiveis: InformacoesSensiveis
    comunicacao: Optional[Comunicacao] = None
    localizacao: Optional[Localizacao] = None
    
    senha: str
    confirmacao_senha: str
    salt: Optional[str] = None

class PessoaJuridica(LGPDBaseModel):

    nome_fantasia: str
    cnpj: str
    inscricao_estadual: Optional[str] = None

    basicos: Basicos
    comunicacao: Optional[Comunicacao] = None
    localizacao: Optional[Localizacao] = None

class CriarPessoaJuridica(LGPDBaseModel):

    nome_fantasia: str
    cnpj: str
    inscricao_estadual: Optional[str] = None

    basicos: Basicos
    comunicacao: Optional[Comunicacao] = None
    localizacao: Optional[Localizacao] = None

    senha: str
    confirmacao_senha: str
    salt: Optional[str] = None


class Permissao(LGPDBaseModel):
    id_pessoa: PydanticObjectId
    id_pessoa_juridica: PydanticObjectId

    dados_basicos: bool = False
    dados_sensiveis: bool = False
    comunicacao: bool = False
    localizacao: bool = False

    aprovada: bool = False
