-- Migration Phase 3: Module Rédaction d'Actes (Templates)
-- Date: 2025-12-09

-- 1. Table Templates
CREATE TABLE IF NOT EXISTS templates (
    id SERIAL PRIMARY KEY,
    nom VARCHAR(200) NOT NULL UNIQUE,
    description TEXT,
    contenu TEXT NOT NULL, -- Contenu avec variables {{variable}}
    type_acte VARCHAR(50) NOT NULL, -- VENTE, PROCURATION, SUCCESSION, etc.
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 2. Insertion de quelques templates de base (Exemples)
INSERT INTO templates (nom, type_acte, description, contenu) 
VALUES 
(
    'Procuration Générale', 
    'PROCURATION',
    'Modèle standard de procuration générale',
    'JE SOUSSIGNÉ(E), {{nom_mandant}}, né(e) le {{date_naissance_mandant}} à {{lieu_naissance_mandant}}, demeurant à {{adresse_mandant}},

DONNE POUVOIR par les présentes à :

M. {{nom_mandataire}}, né(e) le {{date_naissance_mandataire}}, demeurant à {{adresse_mandataire}},

DE :
Gérer et administrer tous ses biens, meubles et immeubles...

FAIT À {{ville_signature}}, LE {{date_signature}}.'
) 
ON CONFLICT (nom) DO NOTHING;

INSERT INTO templates (nom, type_acte, description, contenu) 
VALUES 
(
    'Reconnaissance de Dette', 
    'PRET',
    'Reconnaissance de dette simple entre particuliers',
    'JE SOUSSIGNÉ(E), {{nom_debiteur}}, reconnais devoir à {{nom_creancier}}, la somme de {{montant_dette}} ({{montant_lettres}}).

Cette somme a été remise ce jour par chèque / virement.

Je m''engage à rembourser cette somme avant le {{date_echeance}}.

FAIT À {{ville_signature}}, LE {{date_signature}}.'
) 
ON CONFLICT (nom) DO NOTHING;


-- 3. Table Actes
CREATE TABLE IF NOT EXISTS actes (
    id SERIAL PRIMARY KEY,
    dossier_id INTEGER NOT NULL REFERENCES dossiers(id) ON DELETE CASCADE,
    template_id INTEGER REFERENCES templates(id),
    titre VARCHAR(255) NOT NULL,
    contenu TEXT,
    statut VARCHAR(50) DEFAULT 'BROUILLON', -- BROUILLON, FINALISE, SIGNE
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);
