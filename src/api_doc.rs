use utoipa::OpenApi;

#[derive(OpenApi)]
#[openapi(
    paths(
        crate::handlers::index,
        crate::handlers::echo,
        crate::handlers::create_pessoa_fisica,
        crate::handlers::get_pessoa_fisica,
    ),
    components(
        schemas(
            crate::models::Basicos,
            crate::models::Comunicacao,
            crate::models::CreatePessoaFisicaRequest,
            crate::models::PessoaFisica,
            crate::models::Telefone,
            crate::models::RedesSociais,
            crate::models::Endereco,
            crate::models::Localizacao,
        )
    ),
    tags(
        (name = "Pessoas", description = "Operações relacionadas a pessoas físicas"),
        (name = "Utilities", description = "Utilities and helper endpoints"),
        (name = "Docs", description = "Documentation and UI redirect")
    ),
    info(title = "LGPD REST Prototype", version = "0.1.0")
)]
pub struct ApiDoc;
