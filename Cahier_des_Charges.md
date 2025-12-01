# Cahier des Charges - AGEN-OHADA
**Application de Gestion d'Étude Notariale OHADA**

> **Version :** 1.0.0
> **Date :** 28 Novembre 2025
> **Statut :** Validé

---

## 1. Introduction

### 1.1 Contexte du Projet
L'étude notariale souhaite moderniser son infrastructure informatique en se dotant d'une solution logicielle sur mesure. Les solutions existantes sur le marché (telles que Genapi) sont souvent onéreuses, fermées ou mal adaptées aux spécificités juridiques et fiscales de l'espace OHADA (Organisation pour l'Harmonisation en Afrique du Droit des Affaires).
Le projet AGEN-OHADA vise à combler ce vide en proposant une application web Full-Stack robuste, sécurisée et conforme aux normes en vigueur.

### 1.2 Objectifs
*   **Centralisation :** Regrouper la gestion des dossiers, des actes, des contacts et de la comptabilité en une seule plateforme.
*   **Conformité :** Garantir le respect des Actes Uniformes de l'OHADA et des règles de la profession notariale.
*   **Productivité :** Automatiser la rédaction des actes et le suivi des formalités pour réduire les erreurs et les délais.
*   **Sécurité :** Assurer la confidentialité absolue des données sensibles des clients.

### 1.3 Périmètre (Scope)
Le système couvrira :
*   La gestion électronique des dossiers (GED).
*   La rédaction assistée d'actes notariés.
*   Le suivi des formalités administratives.
*   La comptabilité notariale (Compte Office et Compte Client).
*   La gestion de la relation client (CRM).

---

## 2. Description Générale

### 2.1 Acteurs et Rôles
*   **Notaire Titulaire :** Accès complet, validation finale des actes et de la comptabilité.
*   **Clercs de Notaire :** Création de dossiers, rédaction d'actes, suivi des formalités.
*   **Comptable :** Gestion des flux financiers, facturation, rapprochement bancaire.
*   **Secrétaire :** Accueil, prise de rendez-vous, ouverture de dossiers simples.
*   **Administrateur :** Gestion des utilisateurs, sauvegardes, configuration technique.

### 2.2 Flux de Travail Principal (Workflow)
1.  **Ouverture :** Création du dossier, identification des parties (KYC).
2.  **Instruction :** Collecte des pièces, rédaction de l'avant-projet d'acte.
3.  **Validation :** Revue par le Notaire, envoi du projet aux parties.
4.  **Signature :** Rendez-vous de signature, réception des fonds.
5.  **Formalités :** Enregistrement, publicité foncière.
6.  **Clôture :** Remise des titres, reddition de comptes, archivage.

---

## 3. Spécifications Fonctionnelles

### 3.1 Module Gestion des Dossiers
*   **Création de Dossier :** Formulaire complet (Nature du dossier, Références). Numérotation automatique séquentielle.
*   **Fiche Client (CRM) :** Gestion des personnes physiques (État civil complet) et morales (RCCM, Représentants). Détection des doublons.
*   **Tableau de Bord :** Vue kanban ou liste des dossiers par statut (Ouvert, En rédaction, En attente de signature, En formalité, Clôturé).
*   **GED Intégrée :** Upload et classement des pièces jointes (PDF, Images) par dossier.

### 3.2 Module Rédaction d'Actes
*   **Bibliothèque de Modèles :** Création et gestion de templates (Vente, Crédit-bail, Testament, Procuration).
*   **Fusion de Données :** Remplissage automatique des variables du modèle (Noms des parties, dates, montants) à partir des données du dossier.
*   **Éditeur de Texte :** Éditeur riche intégré pour l'ajustement des clauses spécifiques.
*   **Versionning :** Historique des modifications pour chaque acte.

### 3.3 Module Formalités
*   **Calculateur de Frais :** Moteur de calcul intégrant les barèmes officiels (Émoluments proportionnels/fixes, Droits d'enregistrement, TVA).
*   **Suivi des Dépôts :** Traçabilité des dépôts aux administrations (Greffe, Impôts, Cadastre) avec dates et numéros de quittance.
*   **Alertes :** Notifications sur les délais légaux de rigueur.

### 3.4 Module Comptabilité Notariale
*   **Ségrégation des Fonds :** Distinction stricte et imperméable entre les fonds de l'étude et les fonds détenus pour le compte de tiers (Clients).
*   **Plan Comptable :** Intégration du plan comptable notarial spécifique.
*   **Opérations :** Saisie des encaissements (Chèque, Virement, Espèces) et décaissements.
*   **Taxation :** Génération automatique des factures et reçus à partir du calculateur de frais.
*   **États :** Balance âgée, Grand Livre, Relevés de compte client individuels.

---

## 4. Exigences Non-Fonctionnelles

### 4.1 Sécurité
*   **Authentification :** Support de l'authentification à deux facteurs (2FA).
*   **Chiffrement :** Chiffrement des données sensibles en base (AES-256) et communications via HTTPS (TLS 1.3).
*   **Sauvegardes :** Système de backup automatisé quotidien avec rétention définie.

### 4.2 Performance
*   Interface réactive (Single Page Application).
*   Support de plusieurs utilisateurs simultanés sans dégradation de performance.

### 4.3 Conformité
*   Respect des normes RGPD pour les données personnelles.
*   Traçabilité complète (Audit Log) de toutes les actions critiques (suppression, modification comptable).

---

## 5. Architecture Technique

### 5.1 Stack Technologique
*   **Backend & Frontend :** RIO Framework (Python). Rio permet de développer l'intégralité de l'application (UI et Logique) en Python pur, facilitant la maintenance et la cohérence.
*   **Base de Données :** PostgreSQL. Choisi pour sa robustesse, sa conformité ACID et sa capacité à gérer des relations complexes et des données JSON si nécessaire.
*   **Hébergement :** Serveur dédié ou Cloud Privé (VPS) sous Linux (Ubuntu/Debian).

### 5.2 Modèle de Données Détaillé

Le schéma de base de données relationnel (PostgreSQL) sera structuré autour des entités principales suivantes :

#### 5.2.1 Gestion des Utilisateurs et Droits (`Users`)
*   **Users** : `id`, `username`, `password_hash`, `email`, `role` (Notaire, Clerc, Comptable, Admin), `created_at`, `last_login`.
*   **Permissions** : `id`, `user_id`, `resource`, `action` (Read, Write, Delete).

#### 5.2.2 Répertoire et Clients (`CRM`)
*   **Clients** :
    *   `id`
    *   `type` (Physique, Morale)
    *   `nom` / `raison_sociale`
    *   `prenom` (si physique)
    *   `date_naissance` / `date_creation`
    *   `lieu_naissance` / `siege_social`
    *   `adresse`, `telephone`, `email`
    *   `identifiant_unique` (NINA, RCCM, NINEA...)
*   **Contacts** : `id`, `client_id`, `nom`, `fonction` (pour les personnes morales).

#### 5.2.3 Gestion des Dossiers (`Dossiers`)
*   **Dossiers** :
    *   `id`
    *   `numero_dossier` (Format: ANNEE-MOIS-SEQ ex: 2024-11-001)
    *   `intitule` (ex: "Vente Immeuble X")
    *   `type_dossier` (Vente, Succession, Donation...)
    *   `statut` (Ouvert, Instruction, Signature, Formalité, Clôturé)
    *   `date_ouverture`, `date_cloture`
    *   `responsable_id` (FK vers Users)
*   **Dossier_Parties** : Table de liaison `dossier_id`, `client_id`, `role_dans_acte` (Vendeur, Acquéreur, Bailleur, Preneur...).

#### 5.2.4 Actes et Documents (`Actes`)
*   **Actes** :
    *   `id`
    *   `dossier_id`
    *   `type_acte`
    *   `contenu_json` (Données structurées pour la fusion)
    *   `contenu_html` (Texte rédigé)
    *   `statut` (Brouillon, Validé, Signé)
    *   `date_signature`
*   **Versions_Actes** : Historique des modifications (`acte_id`, `contenu`, `modified_by`, `timestamp`).
*   **Documents** : `id`, `dossier_id`, `type` (Pièce d'identité, Titre Foncier...), `chemin_fichier`, `hash`.

#### 5.2.5 Comptabilité Notariale (`Compta`)
*   **Comptes** :
    *   `id`
    *   `numero_compte` (Plan comptable)
    *   `libelle`
    *   `type` (Général, Client, Tiers)
*   **Sous_Comptes_Clients** :
    *   `id`
    *   `client_id`
    *   `dossier_id` (Optionnel, pour sous-compte affaire)
    *   `solde_actuel`
*   **Ecritures** :
    *   `id`
    *   `date_ecriture`
    *   `libelle_operation`
    *   `dossier_id` (Lien vers le dossier concerné)
    *   `journal_code` (Banque, Caisse, OD)
    *   `valide` (Booléen)
*   **Mouvements** :
    *   `id`
    *   `ecriture_id`
    *   `compte_id`
    *   `debit`
    *   `credit`

#### 5.2.6 Formalités et Taxe (`Formalites`)
*   **Formalites** :
    *   `id`
    *   `dossier_id`
    *   `type_formalite` (Enregistrement, Publication...)
    *   `date_depot`, `date_retour`
    *   `cout_estime`, `cout_reel`
    *   `reference_externe` (Numéro de quittance)

---

## 6. Planning Prévisionnel (Macro)
1.  **Phase 1 :** Socle technique, Gestion des Utilisateurs et Gestion des Dossiers (MVP).
2.  **Phase 2 :** Module Rédaction d'Actes et Base de données Clients.
3.  **Phase 3 :** Comptabilité Notariale et Formalités.
4.  **Phase 4 :** Tests, Recette et Déploiement.
