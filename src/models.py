import uuid
from bson.objectid import ObjectId as BsonObjectId
from pydantic import BaseModel, Field
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
    def __get_pydantic_json_schema__(cls, core_schema) -> Dict[str, Any]:
        """
        Pydantic v2 hook to provide JSON Schema for this custom type.
        Represent ObjectId as a string in the OpenAPI / JSON schema.
        """
        return {"type": "string", "format": "objectid", "example": "650b9c8f2f9b5a1b2c3d4e5f"}


# Common base model to include json encoders for ObjectId (Pydantic v2)
class LGPDBaseModel(BaseModel):
    model_config = {
        "arbitrary_types_allowed": True,
        "json_encoders": {BsonObjectId: lambda v: str(v)},
    }


class Basicos(LGPDBaseModel):
    name: str
    email: str
    login: str


class InformacoesSensiveis(LGPDBaseModel):
    cpf: Optional[str] = None
    rg: Optional[str] = None


class Telefone(LGPDBaseModel):
    numero: str
    tipo: str


class RedesSociais(LGPDBaseModel):
    plataforma: str
    username: str


class Endereco(LGPDBaseModel):
    numero: str
    rua: str
    bairro: str
    cidade: str
    estado: str
    cep: str
    pais: str


class Comunicacao(LGPDBaseModel):
    telefones: Optional[List[Telefone]] = None
    fax: Optional[str] = None
    redes_sociais: Optional[List[RedesSociais]] = None
    site: Optional[str] = None


class Localizacao(LGPDBaseModel):
    enderecos: Optional[List[Endereco]] = None


class PessoaFisica(LGPDBaseModel):
    id: PydanticObjectId = Field(alias='_id', serialization_alias='id')
    basicos: Basicos
    informacoes_sensiveis: InformacoesSensiveis
    comunicacao: Optional[Comunicacao] = None
    localizacao: Optional[Localizacao] = None
    senha: str
    confirmacao_senha: str


class PessoaJuridica(LGPDBaseModel):
    id: PydanticObjectId = Field(alias='_id', serialization_alias='id')

    nome_fantasia: str
    cnpj: str
    inscricao_estadual: Optional[str] = None

    basicos: Basicos
    comunicacao: Optional[Comunicacao] = None
    localizacao: Optional[Localizacao] = None

    senha: str
    confirmacao_senha: str


class Permissao(LGPDBaseModel):
    id: PydanticObjectId = Field(alias='_id', serialization_alias='id')
    id_pessoa: PydanticObjectId
    id_pessoa_juridica: PydanticObjectId

    dados_basicos: bool = False
    dados_sensiveis: bool = False
    comunicacao: bool = False
    localizacao: bool = False
