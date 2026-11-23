-- PostgreSQL : cinq emplacements de sauvegarde indépendants.
CREATE TABLE IF NOT EXISTS sauvegardes (
    slot INTEGER PRIMARY KEY CHECK (slot BETWEEN 1 AND 5),
    x INTEGER NOT NULL,
    y INTEGER NOT NULL,
    vies INTEGER NOT NULL CHECK (vies >= 0),
    score INTEGER NOT NULL CHECK (score >= 0),
    niveau VARCHAR(100) NOT NULL DEFAULT 'niveau_1',
    gagne BOOLEAN NOT NULL DEFAULT FALSE,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);
