mod api_doc;
mod handlers;
mod models;
mod db;

use actix_web::{web, App, HttpServer};
use api_doc::ApiDoc;
use handlers::{create_pessoa_fisica, get_pessoa_fisica, echo, index};
use std::net::Ipv4Addr;
use utoipa::OpenApi;
use utoipa_swagger_ui::SwaggerUi;

const PORT: u16 = 8989;

#[actix_web::main]
async fn main() -> std::io::Result<()> {
    // Load .env if present
    dotenvy::dotenv().ok();

    // Read DATABASE_URL from environment
    let database_url = std::env::var("DATABASE_URL")
        .expect("DATABASE_URL must be set in env to connect to DB");
    print!("Using DATABASE_URL: {}\n", database_url);
    // Initialize the DB pool (returns sqlx::PgPool)
    let pool = db::init_pool(&database_url)
        .await
        .expect("Failed to create DB pool");

    println!("Starting LGPD REST API server on http://localhost:{}", PORT);
    println!(
        "Swagger UI available at: http://localhost:{}/swagger-ui/",
        PORT
    );

    HttpServer::new(move || {
        App::new()
            // make the pool available to handlers via web::Data<PgPool>
            .app_data(web::Data::new(pool.clone()))
            .service(index)
            .service(echo)
            .service(get_pessoa_fisica)
            .service(create_pessoa_fisica)
            .service(
                SwaggerUi::new("/swagger-ui/{_:.*}")
                    .url("/api-docs/openapi.json", ApiDoc::openapi()),
            )
    })
    .bind((Ipv4Addr::UNSPECIFIED, PORT))?
    .run()
    .await
}
