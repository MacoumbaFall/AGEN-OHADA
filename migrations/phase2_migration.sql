-- Comprehensive migration script for Phase 2 features
-- Date: 2025-12-08
-- Purpose: Add missing columns and tables for Phase 2 (Options B, C, D)

-- 1. Add financial columns to dossiers table
ALTER TABLE dossiers 
ADD COLUMN IF NOT EXISTS montant_acte DECIMAL(15, 2),
ADD COLUMN IF NOT EXISTS emoluments DECIMAL(15, 2),
ADD COLUMN IF NOT EXISTS debours DECIMAL(15, 2),
ADD COLUMN IF NOT EXISTS description TEXT;

-- 2. Create dossier_historique table (Option C: Status History)
CREATE TABLE IF NOT EXISTS dossier_historique (
    id SERIAL PRIMARY KEY,
    dossier_id INTEGER REFERENCES dossiers(id) ON DELETE CASCADE,
    ancien_statut VARCHAR(30),
    nouveau_statut VARCHAR(30) NOT NULL,
    date_changement TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    user_id INTEGER REFERENCES users(id),
    commentaire TEXT
);

-- 3. Create documents table (Option D: Document Management)
CREATE TABLE IF NOT EXISTS documents (
    id SERIAL PRIMARY KEY,
    dossier_id INTEGER REFERENCES dossiers(id) ON DELETE CASCADE,
    titre VARCHAR(200) NOT NULL,
    type_document VARCHAR(50) NOT NULL,
    chemin_fichier VARCHAR(500) NOT NULL,
    date_upload TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    taille_fichier INTEGER
);

-- 4. Create indexes for performance
CREATE INDEX IF NOT EXISTS idx_dossier_historique_dossier ON dossier_historique(dossier_id);
CREATE INDEX IF NOT EXISTS idx_documents_dossier ON documents(dossier_id);

-- Display confirmation
SELECT 'Phase 2 migration completed successfully!' AS status;
