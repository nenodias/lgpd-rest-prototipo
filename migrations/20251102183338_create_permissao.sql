-- Add migration script here
CREATE TABLE IF NOT EXISTS permissao (
  id UUID PRIMARY KEY,
  data JSONB NOT NULL,
  id_pessoa_fisica UUID NOT NULL,
  id_pessoa_juridica UUID NOT NULL,
  basicos bool,
  localizacao bool,
  comunicacao bool,
  created_at TIMESTAMPTZ DEFAULT now()
);