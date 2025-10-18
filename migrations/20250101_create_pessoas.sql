-- ...existing code...
CREATE TABLE IF NOT EXISTS pessoas (
  id UUID PRIMARY KEY,
  data JSONB NOT NULL,
  created_at TIMESTAMPTZ DEFAULT now()
);