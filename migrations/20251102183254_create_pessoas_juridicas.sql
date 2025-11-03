-- Add migration script here
CREATE TABLE IF NOT EXISTS pessoas_juridicas (
  id UUID PRIMARY KEY,
  password varchar(100) NOT NULL,
  salt varchar(100) NOT NULL,
  data JSONB NOT NULL,
  created_at TIMESTAMPTZ DEFAULT now()
);