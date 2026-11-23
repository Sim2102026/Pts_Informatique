"""Accès PostgreSQL aux cinq emplacements de sauvegarde du Platformer.

Configuration Windows PowerShell :
$env:DATABASE_URL="postgresql://postgres:motdepasse@localhost:5432/platformer"
"""
import os
from contextlib import contextmanager

import psycopg

CREATE_TABLE_SQL = """
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
"""


def database_url():
    url = os.getenv("DATABASE_URL")
    if not url:
        raise RuntimeError(
            "DATABASE_URL n'est pas définie. Exemple : "
            "postgresql://postgres:motdepasse@localhost:5432/platformer"
        )
    return url


@contextmanager
def connexion():
    with psycopg.connect(database_url()) as conn:
        yield conn


def initialiser_base():
    """Crée la table à cinq slots et migre l'ancienne sauvegarde unique si nécessaire."""
    with connexion() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT column_name
                FROM information_schema.columns
                WHERE table_schema = 'public' AND table_name = 'sauvegardes'
            """)
            colonnes = {ligne[0] for ligne in cur.fetchall()}

            # Ancienne version : table avec nom_partie et un seul slot autosave.
            if colonnes and "slot" not in colonnes:
                cur.execute("""
                    SELECT EXISTS (
                        SELECT 1 FROM information_schema.tables
                        WHERE table_schema = 'public'
                          AND table_name = 'sauvegardes_ancienne'
                    )
                """)
                ancienne_existe = cur.fetchone()[0]
                if ancienne_existe:
                    raise RuntimeError(
                        "La table sauvegardes utilise l'ancien format et "
                        "sauvegardes_ancienne existe déjà. Sauvegardez la base "
                        "puis effectuez la migration manuellement."
                    )
                cur.execute("ALTER TABLE sauvegardes RENAME TO sauvegardes_ancienne")

            cur.execute(CREATE_TABLE_SQL)

            if colonnes and "slot" not in colonnes:
                cur.execute("""
                    INSERT INTO sauvegardes
                        (slot, x, y, vies, score, niveau, gagne, updated_at)
                    SELECT 1, x, y, vies, score, niveau, gagne, updated_at
                    FROM sauvegardes_ancienne
                    WHERE nom_partie = 'autosave'
                    ORDER BY updated_at DESC
                    LIMIT 1
                    ON CONFLICT (slot) DO NOTHING
                """)


def lister_sauvegardes():
    """Retourne toujours les cinq slots, avec None pour les emplacements vides."""
    resultat = {slot: None for slot in range(1, 6)}
    sql = """
        SELECT slot, x, y, vies, score, niveau, gagne, updated_at
        FROM sauvegardes ORDER BY slot
    """
    with connexion() as conn:
        with conn.cursor() as cur:
            cur.execute(sql)
            for ligne in cur.fetchall():
                resultat[ligne[0]] = {
                    "slot": ligne[0], "x": ligne[1], "y": ligne[2],
                    "vies": ligne[3], "score": ligne[4], "niveau": ligne[5],
                    "gagne": ligne[6], "updated_at": ligne[7],
                }
    return resultat


def charger_sauvegarde(slot):
    """Charge un slot (1 à 5), ou renvoie None s'il est vide."""
    _verifier_slot(slot)
    sql = """
        SELECT slot, x, y, vies, score, niveau, gagne, updated_at
        FROM sauvegardes WHERE slot = %s
    """
    with connexion() as conn:
        with conn.cursor() as cur:
            cur.execute(sql, (slot,))
            ligne = cur.fetchone()
    if ligne is None:
        return None
    return {
        "slot": ligne[0], "x": ligne[1], "y": ligne[2], "vies": ligne[3],
        "score": ligne[4], "niveau": ligne[5], "gagne": ligne[6],
        "updated_at": ligne[7],
    }


def sauvegarder(slot, joueur, niveau="niveau_1", gagne=False):
    """Crée ou met à jour uniquement l'emplacement demandé."""
    _verifier_slot(slot)
    sql = """
        INSERT INTO sauvegardes
            (slot, x, y, vies, score, niveau, gagne, updated_at)
        VALUES (%s, %s, %s, %s, %s, %s, %s, CURRENT_TIMESTAMP)
        ON CONFLICT (slot) DO UPDATE SET
            x = EXCLUDED.x, y = EXCLUDED.y, vies = EXCLUDED.vies,
            score = EXCLUDED.score, niveau = EXCLUDED.niveau,
            gagne = EXCLUDED.gagne, updated_at = CURRENT_TIMESTAMP
    """
    with connexion() as conn:
        with conn.cursor() as cur:
            cur.execute(sql, (
                slot, joueur.rect.x, joueur.rect.y, joueur.vies,
                joueur.score, niveau, gagne,
            ))


def supprimer_sauvegarde(slot):
    _verifier_slot(slot)
    with connexion() as conn:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM sauvegardes WHERE slot = %s", (slot,))


def _verifier_slot(slot):
    if isinstance(slot, bool) or not isinstance(slot, int) or not 1 <= slot <= 5:
        raise ValueError("Le numéro d'emplacement doit être compris entre 1 et 5.")
