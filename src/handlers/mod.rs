use crate::models::{Basicos, CreatePessoaFisicaRequest, PessoaFisica};
use actix_web::{HttpResponse, Responder, get, post, web};
use uuid::Uuid;
use sqlx::{PgPool, Row};

#[utoipa::path(
    get,
    path = "/",
    tag = "Docs",
    responses(
        (status = 302, description = "Redirects to the Swagger UI")
    )
)]
#[get("/")]
pub async fn index() -> impl Responder {
    HttpResponse::Found()
        .append_header(("Location", "/swagger-ui/"))
        .finish()
}

#[utoipa::path(
    post,
    path = "/echo",
    tag = "Utilities",
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
    tag = "Pessoas",
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

    // Create the Basicos struct (no id here)
    let basicos = Basicos {
        nome: pessoa_request.nome.clone(),
        email: pessoa_request.email.clone(),
        login: pessoa_request.login.clone(),
    };

    // Create the complete PessoaFisica with top-level id
    let pessoa_fisica = PessoaFisica {
        id,
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
    path = "/pessoa-fisica/{id}",
    tag = "Pessoas",
    params(
        // changed: document id as a uuid-formatted string to avoid requiring `Uuid: ToSchema`
        ("id" = String, Path, description = "UUID of the PessoaFisica", example = "550e8400-e29b-41d4-a716-446655440000", format = "uuid")
    ),
    responses(
        (status = 200, description = "Pessoa física encontrada", body = PessoaFisica),
        (status = 404, description = "Pessoa não encontrada"),
        (status = 500, description = "DB or deserialization error")
    )
)]
#[get("/pessoa-fisica/{id}")]
pub async fn get_pessoa_fisica(
    pool: web::Data<PgPool>,
    id: web::Path<Uuid>,
) -> impl Responder {
    println!("Fetching PessoaFisica with id: {}\n", id);
    let id = id.into_inner();
    match sqlx::query("SELECT data FROM pessoas WHERE id = $1")
        .bind(id)
        .fetch_optional(pool.get_ref())
        .await
    {
        Ok(Some(row)) => {
            let value: serde_json::Value = row.get("data");
            match serde_json::from_value::<PessoaFisica>(value) {
                Ok(pessoa) => HttpResponse::Ok().json(pessoa),
                Err(e) => {
                    eprintln!("Deserialization error: {:?}", e);
                    HttpResponse::InternalServerError().body("Deserialization error")
                }
            }
        }
        Ok(None) => HttpResponse::NotFound().body("Pessoa not found"),
        Err(e) => {
            eprintln!("DB query error: {:?}", e);
            HttpResponse::InternalServerError().body("Database error")
        }
    }
}
