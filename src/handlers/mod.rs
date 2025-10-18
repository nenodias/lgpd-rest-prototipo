use crate::models::{Basicos, CreatePessoaFisicaRequest, PessoaFisica};
use actix_web::{HttpResponse, Responder, get, post, web};
use uuid::Uuid;
use sqlx::PgPool;

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
    pool: web::Data<PgPool>,
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

    // persist as jsonb in table `pessoas`
    match serde_json::to_value(&pessoa_fisica) {
        Ok(json_value) => {
            let res = sqlx::query("INSERT INTO pessoas (id, data) VALUES ($1, $2)")
                .bind(id)
                .bind(json_value)
                .execute(pool.get_ref())
                .await;
            if let Err(e) = res {
                eprintln!("DB insert error: {:?}", e);
                return HttpResponse::InternalServerError().body("Failed to save to DB");
            }
            HttpResponse::Created().json(pessoa_fisica)
        }
        Err(e) => {
            eprintln!("Serialization error: {:?}", e);
            HttpResponse::InternalServerError().body("Serialization error")
        }
    }
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
