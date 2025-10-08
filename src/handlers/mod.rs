use crate::models::{Basicos, CreatePessoaFisicaRequest, PessoaFisica};
use actix_web::{HttpResponse, Responder, get, post, web};
use uuid::Uuid;

#[utoipa::path(
    get,
    path = "/",
    responses(
        (status = 200, description = "Returns 'Hello world!'")
    )
)]
#[get("/")]
pub async fn hello() -> impl Responder {
    HttpResponse::Ok().body("Hello world!")
}

#[utoipa::path(
    post,
    path = "/echo",
    request_body = String,
    responses(
        (status = 200, description = "Echoes back the posted string")
    )
)]
#[post("/echo")]
pub async fn echo(req_body: String) -> impl Responder {
    HttpResponse::Ok().body(req_body)
}

#[utoipa::path(
    post,
    path = "/pessoa-fisica",
    request_body = CreatePessoaFisicaRequest,
    responses(
        (status = 201, description = "Pessoa física criada com sucesso", body = PessoaFisica),
        (status = 400, description = "Dados inválidos")
    )
)]
#[post("/pessoa-fisica")]
pub async fn create_pessoa_fisica(
    pessoa_request: web::Json<CreatePessoaFisicaRequest>,
) -> impl Responder {
    // Generate a new UUID for the person
    let id = Uuid::new_v4();

    // Create the Basicos struct with the generated ID
    let basicos = Basicos {
        id,
        nome: pessoa_request.nome.clone(),
        email: pessoa_request.email.clone(),
        login: pessoa_request.login.clone(),
    };

    // Create the complete PessoaFisica
    let pessoa_fisica = PessoaFisica {
        basicos,
        comunicacao: pessoa_request.comunicacao.clone(),
        localizacoes: pessoa_request.localizacoes.clone(),
    };

    // In a real application, you would save this to a database here
    // For now, we'll just return the created person

    HttpResponse::Created().json(pessoa_fisica)
}

#[utoipa::path(
    get,
    path = "/hey",
    responses(
        (status = 200, description = "Returns Hey there!")
    )
)]
pub async fn manual_hello() -> impl Responder {
    HttpResponse::Ok().body("Hey there!")
}
