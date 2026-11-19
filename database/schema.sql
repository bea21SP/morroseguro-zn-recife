-- Extensão espacial PostGIS
CREATE EXTENSION IF NOT EXISTS postgis;

CREATE TABLE IF NOT EXISTS chamados_oficiais (
    id VARCHAR(50) PRIMARY KEY,
    orgao VARCHAR(30) NOT NULL, -- DEFESA_CIVIL ou EMLURB
    bairro VARCHAR(80) NOT NULL,
    rpa VARCHAR(10) NOT NULL, -- RPA 2 ou RPA 3
    descricao TEXT,
    status VARCHAR(80),
    geom GEOMETRY(Point, 4326),
    atualizado_em TIMESTAMP DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS relatos_cidadaos (
    id SERIAL PRIMARY KEY,
    bairro VARCHAR(80) NOT NULL,
    rpa VARCHAR(10) NOT NULL,
    titulo_ia VARCHAR(180) NOT NULL,
    categoria_ia VARCHAR(60) NOT NULL,
    urgencia VARCHAR(20) NOT NULL,
    afeta_transporte BOOLEAN DEFAULT FALSE,
    resumo_tecnico TEXT,
    geom GEOMETRY(Point, 4326) NOT NULL,
    criado_em TIMESTAMP DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_chamados_geom ON chamados_oficiais USING GIST (geom);
CREATE INDEX IF NOT EXISTS idx_relatos_geom ON relatos_cidadaos USING GIST (geom);

-- Consulta espacial: agrupar relatos em raio de 30 metros para validar urgência comunitária
SELECT a.id, a.bairro, a.titulo_ia, COUNT(b.id) AS total_confirmacoes_30m
FROM relatos_cidadaos a
JOIN relatos_cidadaos b ON ST_DWithin(a.geom::geography, b.geom::geography, 30)
GROUP BY a.id, a.bairro, a.titulo_ia;