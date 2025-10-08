# LGPD REST API Prototype

This is a Rust REST API prototype for managing personal data in compliance with LGPD (Lei Geral de Proteção de Dados).

## Features

- POST endpoint for creating `PessoaFisica` records
- Comprehensive data structure for personal information
- Swagger UI documentation
- JSON serialization/deserialization

## Data Structure

The `PessoaFisica` struct contains:

### Basicos
- `id`: UUID (auto-generated)
- `nome`: String
- `email`: String  
- `login`: String

### Comunicacao
- `telefones`: List of phone numbers with type
- `fax`: Optional fax number
- `site`: Optional website
- `redes_sociais`: List of social media accounts

### Localizacoes
- List of addresses with:
  - `rua`: Street
  - `numero`: Number
  - `bairro`: Neighborhood
  - `cidade`: City
  - `uf`: State
  - `pais`: Country

## Running the Server

```bash
cargo run
```

The server will start on `http://localhost:8989`

## API Documentation

Access the Swagger UI at: `http://localhost:8989/swagger-ui/`

## Endpoints

### POST /pessoa-fisica

Creates a new PessoaFisica record.

**Request Body Example:**
```json
{
  "nome": "João Silva",
  "email": "joao.silva@example.com",
  "login": "joao_silva",
  "comunicacao": {
    "telefones": [
      {
        "numero": "+55 11 99999-9999",
        "tipo": "celular"
      }
    ],
    "fax": "+55 11 4444-4444",
    "site": "https://joaosilva.com.br",
    "redes_sociais": [
      {
        "plataforma": "LinkedIn",
        "usuario": "joao-silva-dev"
      }
    ]
  },
  "localizacoes": [
    {
      "endereco": {
        "rua": "Rua das Flores",
        "numero": "123",
        "bairro": "Centro",
        "cidade": "São Paulo",
        "uf": "SP",
        "pais": "Brasil"
      }
    }
  ]
}
```

**Response:**
- Status: 201 Created
- Body: Complete PessoaFisica object with generated UUID

## Testing

Use the provided `example_request.json` file to test the endpoint:

```bash
curl -X POST http://localhost:8989/pessoa-fisica \
  -H "Content-Type: application/json" \
  -d @example_request.json
```

## Dependencies

- `actix-web`: Web framework
- `utoipa`: OpenAPI documentation
- `serde`: JSON serialization
- `uuid`: UUID generation