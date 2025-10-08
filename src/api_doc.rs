use crate::models::{
    Basicos, Comunicacao, CreatePessoaFisicaRequest, Endereco, Localizacao, PessoaFisica,
    RedesSociais, Telefone,
};
use utoipa::OpenApi;

#[derive(OpenApi)]
#[openapi(
    paths(
        crate::handlers::hello,
        crate::handlers::echo,
        crate::handlers::manual_hello,
        crate::handlers::create_pessoa_fisica
    ),
    components(
        schemas(Basicos, Telefone, RedesSociais, Comunicacao, Endereco, Localizacao, PessoaFisica, CreatePessoaFisicaRequest)
    ),
    tags(
        (name = "lgpd", description = "LGPD management endpoints.")
    ),
)]
pub struct ApiDoc;
