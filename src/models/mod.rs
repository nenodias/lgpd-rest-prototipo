use serde::{Deserialize, Serialize};
use utoipa::ToSchema;
use uuid::Uuid;

#[derive(Serialize, Deserialize, ToSchema, Clone, Debug)]
pub struct Basicos {
    pub nome: String,
    pub email: String,
    pub login: String,
}

#[derive(Serialize, Deserialize, ToSchema, Clone, Debug)]
pub struct Telefone {
    pub numero: String,
    pub tipo: String, // celular, fixo, comercial, etc.
}

#[derive(Serialize, Deserialize, ToSchema, Clone, Debug)]
pub struct RedesSociais {
    pub plataforma: String, // Facebook, Instagram, LinkedIn, etc.
    pub usuario: String,
}

#[derive(Serialize, Deserialize, ToSchema, Clone, Debug)]
pub struct Comunicacao {
    pub telefones: Vec<Telefone>,
    pub fax: Option<String>,
    pub site: Option<String>,
    pub redes_sociais: Vec<RedesSociais>,
}

#[derive(Serialize, Deserialize, ToSchema, Clone, Debug)]
pub struct Endereco {
    pub rua: String,
    pub numero: String,
    pub bairro: String,
    pub cidade: String,
    pub uf: String,
    pub cep: String,
    pub pais: String,
}

#[derive(Serialize, Deserialize, ToSchema, Clone, Debug)]
pub struct Localizacao {
    pub endereco: Endereco,
}

#[derive(Serialize, Deserialize, ToSchema, Clone, Debug)]
pub struct PessoaFisica {
    /// Represented as a UUID-formatted string in OpenAPI (docs) while remaining `Uuid` at runtime.
    #[schema(value_type = String, format = "uuid", example = "550e8400-e29b-41d4-a716-446655440000")]
    pub id: Uuid,
    pub basicos: Basicos,
    pub comunicacao: Comunicacao,
    pub localizacoes: Vec<Localizacao>,
}

#[derive(Serialize, Deserialize, ToSchema, Clone, Debug)]
pub struct CreatePessoaFisicaRequest {
    pub nome: String,
    pub email: String,
    pub login: String,
    pub comunicacao: Comunicacao,
    pub localizacoes: Vec<Localizacao>,
}
