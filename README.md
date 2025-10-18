# LGPD REST API Prototype

This is a Rust REST API prototype for managing personal data in compliance with LGPD (Lei Geral de Proteção de Dados). The project uses actix-web, sqlx for DB access and utoipa + utoipa-swagger-ui for OpenAPI/Swagger documentation.

## Features

- POST endpoint for creating `PessoaFisica` records
- JSONB persistence for flexible payloads
- Swagger UI documentation (served at `/swagger-ui/`)
- DB migrations using `sqlx-cli`
- Environment-driven configuration (dotenvy)

## Requirements

- Rust (stable)
- Docker & Docker Compose (for local Postgres)
- `sqlx-cli` (for migrations) — see installation below

## Database (local with docker-compose)

A `docker-compose.yml` is included to run Postgres locally. It maps the container port to the host so your app and `sqlx-cli` can connect.

Start the DB:
```bash
docker compose up -d postgres
```

Default env values used by docker-compose (can be overridden in `.env`):
- POSTGRES_USER: `lgpd_user`
- POSTGRES_PASSWORD: `lgpd_password`
- POSTGRES_DB: `lgpd_db`
- POSTGRES_PORT: `5432`

Connect from host:
```bash
psql "postgres://lgpd_user:lgpd_password@127.0.0.1:5432/lgpd_db"
```

## Environment / DATABASE_URL

Create a `.env` in the project root (used by dotenvy/sqlx tooling):

```env
DATABASE_URL=postgres://lgpd_user:lgpd_password@127.0.0.1:5432/lgpd_db
RUST_LOG=info
SERVER_ADDR=0.0.0.0:8989
```

The `DATABASE_URL` must be set for `sqlx-cli` and the running app.

## sqlx / sqlx-cli (migrations)

Install `sqlx-cli` (pick TLS backend matching your build; example uses `rustls`):

Option A (rustls):
```bash
cargo install sqlx-cli --no-default-features --features postgres,rustls
```

Option B (native-tls):
```bash
cargo install sqlx-cli --no-default-features --features postgres,native-tls
```

Verify installation:
```bash
sqlx --version
```

Create and run migrations:

1. Create migrations directory (sqlx will create it on first `migrate add`):
```bash
sqlx migrate add init_create_pessoas_table
```

2. Example migration SQL (place in the generated up.sql):
```sql
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

CREATE TABLE IF NOT EXISTS pessoas (
  id uuid PRIMARY KEY,
  data jsonb NOT NULL,
  created_at timestamptz DEFAULT now()
);
```

3. Run migrations:
```bash
export DATABASE_URL=postgres://lgpd_user:lgpd_password@127.0.0.1:5432/lgpd_db
sqlx migrate run
```

You can also create the DB (if needed) using:
```bash
sqlx database create
```

## Example migration file contents

// migrations/<timestamp>_init_create_pessoas_table/up.sql
```sql
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

CREATE TABLE IF NOT EXISTS pessoas (
  id uuid PRIMARY KEY,
  data jsonb NOT NULL,
  created_at timestamptz DEFAULT now()
);
```

// migrations/<timestamp>_init_create_pessoas_table/down.sql
```sql
DROP TABLE IF EXISTS pessoas;
```

## Running the server

1. Ensure the DB is running and migrations have been applied.
2. Export the DATABASE_URL or ensure `.env` is present.
3. Run:
```bash
cargo run
```

By default the server exposes the API and Swagger UI. Example base URL (project README used previously):
- Server: http://localhost:8989
- Swagger UI: http://localhost:8989/swagger-ui/

(If your main binds to a different port, use that port.)

## API documentation (Swagger)

Open the Swagger UI at:
```
http://localhost:8989/swagger-ui/
```
The root endpoint `/` redirects to the Swagger UI.

## Endpoints

- POST /pessoa-fisica — create a new PessoaFisica (returns 201 with saved object)
- POST /echo — utility that echoes the provided body

See Swagger UI for request/response schemas.

## Testing

Use the provided `example_request.json` to test the POST endpoint:

```bash
curl -X POST http://localhost:8989/pessoa-fisica \
  -H "Content-Type: application/json" \
  -d @example_request.json
```

## Notes & troubleshooting

- Ensure `DATABASE_URL` matches the database credentials and host/port you use (use `127.0.0.1` not `localhost` when connecting from some hosts).
- If `sqlx migrate run` errors about the database connection, confirm Postgres is listening on the mapped port and that `pg_hba.conf` allows host connections.
- For production, restrict `pg_hba.conf` and firewall to limit allowed host IPs; never use `0.0.0.0/0` in production.
- Keep secrets out of source control — use environment variables or a secrets manager.

## Dependencies

- actix-web: HTTP server
- utoipa + utoipa-swagger-ui: OpenAPI documentation and UI
- sqlx: async DB access
- sqlx-cli: migrations (development)
- serde / serde_json: serialization
- uuid: UUID generation
- dotenvy: load .env files

## License / Disclaimer

This is a prototype for learning and demonstration. Treat the DB/schema and security settings accordingly before using in production.