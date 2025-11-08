# LGPD REST API Prototype

Async REST API prototype for managing personal data in compliance with LGPD (Lei Geral de Proteção de Dados).  
Current implementation uses FastAPI, Motor (async MongoDB driver), Pydantic v2 for models, and an authentication middleware. Service is container-friendly via Docker Compose.

## Features

- FastAPI async endpoints for Pessoa Fisica / Pessoa Juridica
- MongoDB persistence (JSON-like documents)
- Pydantic v2 models with custom ObjectId support
- Automatic OpenAPI docs (Swagger UI at `/docs`, ReDoc at `/redoc`)
- Middleware-based auth example
- Docker Compose service for MongoDB

## Requirements

- Python 3.11+ (or supported 3.10)
- Docker & Docker Compose (to run MongoDB)
- Recommended: virtualenv / venv

## Repository layout (important files)
- src/main.py — FastAPI application and startup/shutdown hooks
- src/db.py — Motor connection helpers
- src/models.py — Pydantic v2 models (custom ObjectId type)
- src/endpoints/… — routers for pf/pj endpoints
- docker-compose.yml — MongoDB service for local development
- requirements.txt — Python dependencies (if present)

## Docker (MongoDB)

Start MongoDB via Docker Compose:

```bash
docker compose up -d mongodb
```

Default envs used by compose (can be overridden in `.env`):
- MONGO_INITDB_ROOT_USERNAME: `lgpd_user`
- MONGO_INITDB_ROOT_PASSWORD: `lgpd_password`
- MONGO_INITDB_DATABASE: `lgpd_db`
- MONGO_PORT: `27017`

When running the FastAPI app in the host (outside Docker), use `MONGO_HOST=127.0.0.1`. When running the app in another container in the same compose network, use `MONGO_HOST=mongodb`.

## Environment variables / .env

Create a `.env` in the project root for local development:

```env
MONGO_HOST=mongodb
MONGO_PORT=27017
MONGO_INITDB_ROOT_USERNAME=lgpd_user
MONGO_INITDB_ROOT_PASSWORD=lgpd_password
MONGO_INITDB_DATABASE=lgpd_db

SERVER_HOST=0.0.0.0
SERVER_PORT=8989
```

Notes:
- Use `127.0.0.1` for `MONGO_HOST` when connecting from host to container port-mapped to localhost.
- Never commit secrets; keep `.env` out of VCS.

## Installation (Python)

Create and activate a virtual environment, then install dependencies:

```bash
python -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

requirements.txt should include at least:
- fastapi
- uvicorn[standard]
- motor
- pydantic
- python-dotenv
- pymongo (optional for some utilities)

## Running locally

1. Ensure MongoDB is running (docker compose up -d mongodb)
2. Ensure `.env` has correct values (or export env vars)
3. Start the FastAPI app:

```bash
uvicorn src.main:app --host 0.0.0.0 --port 8989 --reload
```

Open:
- Swagger UI: http://localhost:8989/docs
- ReDoc: http://localhost:8989/redoc

## API Endpoints (examples)

- POST /pessoa_fisica/ — create a PessoaFisica
- GET /pessoa_fisica/{id} — retrieve a PessoaFisica by ObjectId
- POST /pessoa_juridica/ — create a PessoaJuridica
- Other routers under `src/endpoints/` (pf_router, pj_router)

Example: create a PessoaFisica (replace fields with your model shape):

```bash
curl -X POST "http://localhost:8989/pessoa_fisica/" \
  -H "Content-Type: application/json" \
  -d '{"basicos": {"name":"Joao","email":"joao@example.com","login":"joao"}, "informacoes_sensiveis": {"cpf":"12345678900"}}'
```

Example: retrieve by id (use returned `_id` from insert):

```bash
curl "http://localhost:8989/pessoa_fisica/650b9c8f2f9b5a1b2c3d4e5f"
```

## Models & ObjectId handling

- Models use a custom `PydanticObjectId` type (wrapping `bson.ObjectId`) that:
  - Accepts both ObjectId instances and valid hex strings.
  - Serializes to string in JSON responses.
  - Provides a JSON schema representation compatible with Pydantic v2.
- When storing documents in MongoDB, `_id` is used; models typically expose `_id` aliased to `id` or serialize ObjectId to string.

## Troubleshooting

- Connection errors: check `MONGO_HOST` and `MONGO_PORT`. If Mongo runs in Docker and your app runs on host, use `127.0.0.1` and ensure port mapping exists.
- Auth errors: ensure `MONGO_INITDB_ROOT_USERNAME` and `MONGO_INITDB_ROOT_PASSWORD` match what was used when the DB was initialized.
- Pydantic schema errors: ensure code uses Pydantic v2-compatible hooks (`__get_pydantic_json_schema__`) and validators accept extra args.
- Logs: run uvicorn without `--daemon` to see stdout/stderr for startup and handler prints.

## Development notes

- Routers should obtain the DB via FastAPI dependency (e.g., `db: AsyncIOMotorDatabase = Depends(get_db)`), where `get_db` returns `request.app.state.db`.
- App startup connects a single `AsyncIOMotorClient` and stores `app.state.db` and `app.state.mongo_client`.
- Close the client at shutdown to clean up connections.

## License / Disclaimer

Prototype for learning and demonstration. Review security, validation, and data retention policies before any production use.