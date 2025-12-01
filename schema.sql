-- Script de création de la base de données AGEN-OHADA
-- Version: 1.0.0
-- Date: 28/11/2025

-- 1. Création des tables principales

-- Table Users (Utilisateurs)
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    role VARCHAR(20) NOT NULL CHECK (role IN ('NOTAIRE', 'CLERC', 'COMPTABLE', 'ADMIN', 'SECRETAIRE')),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    last_login TIMESTAMP WITH TIME ZONE
);

-- Table Clients (Personnes Physiques et Morales)
CREATE TABLE IF NOT EXISTS clients (
    id SERIAL PRIMARY KEY,
    type_client VARCHAR(20) NOT NULL CHECK (type_client IN ('PHYSIQUE', 'MORALE')),
    nom VARCHAR(100) NOT NULL, -- Nom ou Raison Sociale
    prenom VARCHAR(100), -- NULL si Personne Morale
    date_naissance DATE, -- ou Date de Création pour PM
    lieu_naissance VARCHAR(100), -- ou Siège Social pour PM
    adresse TEXT,
    telephone VARCHAR(30),
    email VARCHAR(100),
    identifiant_unique VARCHAR(50), -- NINA, RCCM, etc.
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Table Dossiers
CREATE TABLE IF NOT EXISTS dossiers (
    id SERIAL PRIMARY KEY,
    numero_dossier VARCHAR(50) UNIQUE NOT NULL, -- Format: ANNEE-MOIS-SEQ
    intitule VARCHAR(200) NOT NULL,
    type_dossier VARCHAR(50), -- Vente, Succession, etc.
    statut VARCHAR(30) DEFAULT 'OUVERT' CHECK (statut IN ('OUVERT', 'INSTRUCTION', 'SIGNATURE', 'FORMALITE', 'CLOTURE', 'ARCHIVE')),
    date_ouverture DATE DEFAULT CURRENT_DATE,
    date_cloture DATE,
    responsable_id INTEGER REFERENCES users(id),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Table de liaison Dossiers <-> Clients (Parties)
CREATE TABLE IF NOT EXISTS dossier_parties (
    dossier_id INTEGER REFERENCES dossiers(id) ON DELETE CASCADE,
    client_id INTEGER REFERENCES clients(id) ON DELETE CASCADE,
    role_dans_acte VARCHAR(50) NOT NULL, -- Vendeur, Acquéreur, etc.
    PRIMARY KEY (dossier_id, client_id)
);

-- Table Actes
CREATE TABLE IF NOT EXISTS actes (
    id SERIAL PRIMARY KEY,
    dossier_id INTEGER REFERENCES dossiers(id) ON DELETE CASCADE,
    type_acte VARCHAR(100) NOT NULL,
    contenu_json JSONB, -- Données structurées
    contenu_html TEXT, -- Texte rédigé
    statut VARCHAR(30) DEFAULT 'BROUILLON' CHECK (statut IN ('BROUILLON', 'VALIDE', 'SIGNE')),
    date_signature DATE,
    version INTEGER DEFAULT 1,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Table Comptabilité - Comptes
CREATE TABLE IF NOT EXISTS compta_comptes (
    id SERIAL PRIMARY KEY,
    numero_compte VARCHAR(20) UNIQUE NOT NULL,
    libelle VARCHAR(100) NOT NULL,
    type_compte VARCHAR(20) NOT NULL CHECK (type_compte IN ('GENERAL', 'CLIENT', 'TIERS'))
);

-- Table Comptabilité - Écritures
CREATE TABLE IF NOT EXISTS compta_ecritures (
    id SERIAL PRIMARY KEY,
    date_ecriture DATE NOT NULL DEFAULT CURRENT_DATE,
    libelle_operation VARCHAR(200) NOT NULL,
    dossier_id INTEGER REFERENCES dossiers(id),
    journal_code VARCHAR(10) NOT NULL, -- BANQUE, CAISSE, OD
    valide BOOLEAN DEFAULT FALSE,
    created_by INTEGER REFERENCES users(id),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Table Comptabilité - Mouvements
CREATE TABLE IF NOT EXISTS compta_mouvements (
    id SERIAL PRIMARY KEY,
    ecriture_id INTEGER REFERENCES compta_ecritures(id) ON DELETE CASCADE,
    compte_id INTEGER REFERENCES compta_comptes(id),
    debit DECIMAL(15, 2) DEFAULT 0,
    credit DECIMAL(15, 2) DEFAULT 0
);

-- Table Formalités
CREATE TABLE IF NOT EXISTS formalites (
    id SERIAL PRIMARY KEY,
    dossier_id INTEGER REFERENCES dossiers(id) ON DELETE CASCADE,
    type_formalite VARCHAR(100) NOT NULL,
    date_depot DATE,
    date_retour DATE,
    cout_estime DECIMAL(12, 2),
    cout_reel DECIMAL(12, 2),
    reference_externe VARCHAR(100), -- Numéro de quittance
    statut VARCHAR(30) DEFAULT 'A_FAIRE'
);

-- Index pour optimiser les recherches
CREATE INDEX idx_dossiers_numero ON dossiers(numero_dossier);
CREATE INDEX idx_clients_nom ON clients(nom);
CREATE INDEX idx_actes_dossier ON actes(dossier_id);
