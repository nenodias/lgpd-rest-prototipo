mod api_doc;
mod handlers;
mod models;

use actix_web::{App, HttpServer, web};
use api_doc::ApiDoc;
use handlers::{create_pessoa_fisica, echo, hello, manual_hello};
use std::net::Ipv4Addr;
use utoipa::OpenApi;
use utoipa_swagger_ui::SwaggerUi;

const PORT: u16 = 8989;

#[actix_web::main]
async fn main() -> std::io::Result<()> {
    println!("Starting LGPD REST API server on http://localhost:{}", PORT);
    println!(
        "Swagger UI available at: http://localhost:{}/swagger-ui/",
        PORT
    );

    HttpServer::new(move || {
        App::new()
            .service(hello)
            .service(echo)
            .service(create_pessoa_fisica)
            .service(
                SwaggerUi::new("/swagger-ui/{_:.*}")
                    .url("/api-docs/openapi.json", ApiDoc::openapi()),
            )
            .route("/hey", web::get().to(manual_hello))
    })
    .bind((Ipv4Addr::UNSPECIFIED, PORT))?
    .run()
    .await
}
