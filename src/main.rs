use actix_web::{App, HttpResponse, HttpServer, Responder, get, post, web};
use std::net::Ipv4Addr;
use utoipa::OpenApi;
use utoipa_swagger_ui::SwaggerUi;

#[utoipa::path(
    get,
    path = "/",
    responses(
        (status = 200, description = "Returns 'Hello world!'")
    )
)]
#[get("/")]
async fn hello() -> impl Responder {
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
async fn echo(req_body: String) -> impl Responder {
    HttpResponse::Ok().body(req_body)
}

#[utoipa::path(
    get,
    path = "/hey",
    responses(
        (status = 200, description = "Returns Hey there!")
    )
)]
async fn manual_hello() -> impl Responder {
    HttpResponse::Ok().body("Hey there!")
}

#[derive(OpenApi)]
#[openapi(
    paths(
        hello,
        echo,
        manual_hello
    ),
    tags(
        (name = "lgpd", description = "LGPD management endpoints.")
    ),
)]
struct ApiDoc;

#[actix_web::main]
async fn main() -> std::io::Result<()> {
    HttpServer::new(move || {
        App::new()
            .service(hello)
            .service(echo)
            .service(
                SwaggerUi::new("/swagger-ui/{_:.*}")
                    .url("/api-docs/openapi.json", ApiDoc::openapi()),
            )
            .route("/hey", web::get().to(manual_hello))
    })
    .bind((Ipv4Addr::UNSPECIFIED, 8989))?
    .run()
    .await
}
