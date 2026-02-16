CREATE TABLE IF NOT EXISTS users (
  id SERIAL PRIMARY KEY,
  first_name TEXT NOT NULL,
  last_name  TEXT NOT NULL,
  email TEXT NOT NULL UNIQUE,
  is_active BOOLEAN NOT NULL DEFAULT TRUE,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

TRUNCATE TABLE users RESTART IDENTITY;

INSERT INTO users (first_name, last_name, email, is_active)
VALUES
('Alito', 'Salas', 'alito@test.com', true),
('Ana', 'Perez', 'ana@test.com', false);
