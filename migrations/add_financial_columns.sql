-- Migration script to add missing financial columns to dossiers table
-- Date: 2025-12-08
-- Purpose: Add montant_acte, emoluments, debours, and description columns

ALTER TABLE dossiers 
ADD COLUMN IF NOT EXISTS montant_acte DECIMAL(15, 2),
ADD COLUMN IF NOT EXISTS emoluments DECIMAL(15, 2),
ADD COLUMN IF NOT EXISTS debours DECIMAL(15, 2),
ADD COLUMN IF NOT EXISTS description TEXT;
