# Plan de Travail - AGEN-OHADA
**Application de Gestion d'Étude Notariale OHADA**

Version: 1.0.0 | Date de création: 01/12/2025

---

## Phase 0 : Configuration de l'Infrastructure (En cours)

### ✅ Complété
- [x] Rédaction et validation du Cahier des Charges (v1.0.0)
- [x] Création de la structure du projet
- [x] Installation de l'environnement virtuel Python
- [x] Installation de Rio Framework
- [x] Création du schéma de base de données SQL
- [x] Configuration des fichiers de base (.gitignore, requirements.txt, README.md)
- [x] Test de l'application Rio (serveur fonctionnel)

### 🔄 En cours
- [ ] Installation de PostgreSQL
- [ ] Initialisation de Git et création du repository GitHub
- [ ] Configuration de la base de données
- [ ] Création des modèles SQLAlchemy

### Durée estimée : 1-2 jours

---

## Phase 1 : Socle Technique et Authentification (MVP) - ✅ TERMINÉ

### Objectif
Mettre en place l'infrastructure de base et le système d'authentification.

### Tâches
1. **Configuration Base de Données**
   - [x] Installer PostgreSQL
   - [x] Créer la base de données `agen_ohada_db`
   - [x] Exécuter le script `schema.sql`
   - [x] Tester la connexion depuis Python

2. **Modèles de Données (SQLAlchemy)**
   - [x] Créer `src/models/__init__.py`
   - [x] Créer `src/models/user.py` (Table Users)
   - [x] Créer `src/models/client.py` (Table Clients)
   - [x] Créer `src/models/dossier.py` (Table Dossiers)
   - [x] Créer la configuration de connexion DB

3. **Système d'Authentification**
   - [x] Page de connexion (Login)
   - [x] Gestion des sessions utilisateur
   - [x] Hashage des mots de passe (bcrypt)
   - [x] Gestion des rôles (NOTAIRE, CLERC, COMPTABLE, etc.)

4. **Interface de Base**
   - [x] Créer le layout principal (Header, Sidebar, Content)
   - [x] Menu de navigation
   - [x] Page d'accueil (Dashboard)

### Livrables
- ✅ Système d'authentification fonctionnel
- ✅ Base de données opérationnelle
- ✅ Interface de base navigable

### Durée estimée : 3-5 jours

---

## Phase 2 : Module Gestion des Dossiers (En cours)

### Objectif
Permettre la création, consultation et gestion des dossiers notariaux.

### Tâches
1. **CRUD Dossiers**
   - [ ] Formulaire de création de dossier
   - [ ] Numérotation automatique (Format: ANNEE-MOIS-SEQ)
   - [ ] Liste des dossiers (avec filtres et recherche)
   - [ ] Fiche détaillée d'un dossier
   - [ ] Modification et suppression de dossier

2. **Gestion des Parties**
   - [ ] Formulaire d'ajout de client (Personne Physique)
   - [ ] Formulaire d'ajout de client (Personne Morale)
   - [ ] Liaison Client <-> Dossier avec rôle (Vendeur, Acquéreur, etc.)
   - [ ] Détection des doublons clients

3. **Statuts et Workflow**
   - [ ] Gestion des statuts (OUVERT, INSTRUCTION, SIGNATURE, etc.)
   - [ ] Changement de statut avec validation
   - [ ] Historique des changements de statut

4. **GED (Gestion Électronique de Documents)**
   - [ ] Upload de fichiers (PDF, Images)
   - [ ] Classement par type de document
   - [ ] Visualisation des documents
   - [ ] Téléchargement

### Livrables
- Module complet de gestion des dossiers
- Base de données clients opérationnelle
- Système de GED fonctionnel

### Durée estimée : 5-7 jours

---

## Phase 3 : Module Rédaction d'Actes

### Objectif
Automatiser la rédaction des actes notariés.

### Tâches
1. **Bibliothèque de Modèles**
   - [ ] Créer la table Templates en DB
   - [ ] Interface de gestion des templates
   - [ ] Système de variables dynamiques ({{nom_vendeur}}, etc.)
   - [ ] Créer 3-5 templates de base (Vente, Procuration, etc.)

2. **Éditeur d'Actes**
   - [ ] Sélection du template
   - [ ] Fusion automatique des données (Data Merging)
   - [ ] Éditeur de texte riche (Rich Text Editor)
   - [ ] Prévisualisation de l'acte

3. **Versionning**
   - [ ] Sauvegarde automatique des versions
   - [ ] Historique des modifications
   - [ ] Comparaison de versions

4. **Export et Impression**
   - [ ] Export en PDF
   - [ ] Mise en page professionnelle
   - [ ] Signature électronique (optionnel)

### Livrables
- Système de templates opérationnel
- Éditeur d'actes fonctionnel
- Export PDF de qualité

### Durée estimée : 5-7 jours

---

## Phase 4 : Module Formalités

### Objectif
Suivre les formalités administratives et calculer les frais.

### Tâches
1. **Calculateur de Frais**
   - [ ] Créer la table Barèmes
   - [ ] Implémenter les règles de calcul OHADA
   - [ ] Calcul des émoluments (proportionnels et fixes)
   - [ ] Calcul des droits d'enregistrement
   - [ ] Calcul de la TVA

2. **Suivi des Formalités**
   - [ ] Créer les formulaires de formalités
   - [ ] Suivi des dépôts (Greffe, Impôts, Cadastre)
   - [ ] Gestion des dates et délais
   - [ ] Alertes automatiques

3. **Documents de Formalités**
   - [ ] Génération des bordereaux
   - [ ] Génération des quittances
   - [ ] Archivage des justificatifs

### Livrables
- Calculateur de frais opérationnel
- Système de suivi des formalités
- Alertes automatiques

### Durée estimée : 4-6 jours

---

## Phase 5 : Module Comptabilité Notariale

### Objectif
Gérer la comptabilité spécifique notariale (Compte Office et Compte Client).

### Tâches
1. **Plan Comptable**
   - [ ] Implémenter le plan comptable notarial
   - [ ] Créer les comptes de base
   - [ ] Gestion des sous-comptes clients

2. **Saisie Comptable**
   - [ ] Formulaire d'encaissement
   - [ ] Formulaire de décaissement
   - [ ] Virements entre comptes
   - [ ] Validation des écritures

3. **États Comptables**
   - [ ] Balance générale
   - [ ] Grand Livre
   - [ ] Relevés de compte client
   - [ ] Balance âgée

4. **Rapprochement Bancaire**
   - [ ] Import des relevés bancaires
   - [ ] Rapprochement automatique
   - [ ] Gestion des écarts

### Livrables
- Système comptable complet
- États comptables réglementaires
- Rapprochement bancaire

### Durée estimée : 7-10 jours

---

## Phase 6 : Tests et Optimisation

### Objectif
Assurer la qualité et la performance de l'application.

### Tâches
1. **Tests Fonctionnels**
   - [ ] Tests de chaque module
   - [ ] Tests d'intégration
   - [ ] Tests de sécurité

2. **Optimisation**
   - [ ] Optimisation des requêtes SQL
   - [ ] Mise en cache
   - [ ] Optimisation du chargement

3. **Documentation**
   - [ ] Documentation technique
   - [ ] Manuel utilisateur
   - [ ] Guide d'installation

### Durée estimée : 3-5 jours

---

## Phase 7 : Déploiement

### Objectif
Mettre l'application en production.

### Tâches
1. **Préparation**
   - [ ] Configuration serveur de production
   - [ ] Migration de la base de données
   - [ ] Configuration SSL/HTTPS

2. **Déploiement**
   - [ ] Déploiement de l'application
   - [ ] Tests en production
   - [ ] Formation des utilisateurs

3. **Maintenance**
   - [ ] Plan de sauvegarde
   - [ ] Monitoring
   - [ ] Support utilisateur

### Durée estimée : 2-3 jours

---

## Calendrier Prévisionnel

| Phase | Durée | Début | Fin |
|-------|-------|-------|-----|
| Phase 0 | 2 jours | J+0 | J+2 |
| Phase 1 | 5 jours | J+2 | J+7 |
| Phase 2 | 7 jours | J+7 | J+14 |
| Phase 3 | 7 jours | J+14 | J+21 |
| Phase 4 | 6 jours | J+21 | J+27 |
| Phase 5 | 10 jours | J+27 | J+37 |
| Phase 6 | 5 jours | J+37 | J+42 |
| Phase 7 | 3 jours | J+42 | J+45 |

**Durée totale estimée : 45 jours (environ 2 mois)**

---

## Prochaines Actions Immédiates

1. ✅ Initialiser Git et créer le repository GitHub
2. ⏳ Installer PostgreSQL
3. ⏳ Configurer la connexion à la base de données
4. ⏳ Créer les premiers modèles SQLAlchemy
5. ⏳ Développer la page de login

---

## Notes Importantes

- **Flexibilité** : Ce planning est indicatif et peut être ajusté selon vos disponibilités
- **Itératif** : Chaque phase peut être testée indépendamment
- **Priorités** : Les phases 1-2 sont critiques pour le MVP
- **Documentation** : Documenter au fur et à mesure du développement
