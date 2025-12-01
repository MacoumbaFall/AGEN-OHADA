# AGEN-OHADA

**Application de Gestion d'Étude Notariale OHADA**

Application Full-Stack développée avec Rio Framework (Python) pour la gestion complète d'une étude notariale conforme aux normes OHADA.

## 📋 Fonctionnalités

- ✅ Gestion des dossiers notariaux
- ✅ Gestion des clients (Personnes physiques et morales)
- ✅ Rédaction assistée d'actes notariés
- ✅ Suivi des formalités administratives
- ✅ Comptabilité notariale (Compte Office et Compte Client)
- ✅ Gestion électronique de documents (GED)

## 🚀 Installation

### Prérequis
- Python 3.11+
- PostgreSQL 14+
- Git

### Étapes

1. **Cloner le repository**
   ```bash
   git clone <url-du-repo>
   cd Projet AGEN-CdC
   ```

2. **Créer un environnement virtuel**
   ```bash
   python -m venv venv
   ```

3. **Activer l'environnement virtuel**
   - Windows: `.\venv\Scripts\activate`
   - Linux/Mac: `source venv/bin/activate`

4. **Installer les dépendances**
   ```bash
   pip install -r requirements.txt
   ```

5. **Configurer la base de données**
   - Copier `.env.example` vers `.env`
   - Modifier les paramètres de connexion PostgreSQL
   - Créer la base de données: `createdb agen_ohada_db`
   - Exécuter le schéma: `psql -d agen_ohada_db -f schema.sql`

## 🏃 Lancement

```bash
python src/main.py
```

L'application sera accessible sur `http://localhost:8000`

## 📚 Documentation

- [Cahier des Charges](Cahier_des_Charges.md)
- [Plan de Travail](PLAN_DE_TRAVAIL.md)

## 🛠️ Stack Technique

- **Framework**: Rio (Python)
- **Base de données**: PostgreSQL
- **ORM**: SQLAlchemy
- **Authentification**: Sessions + Hashage bcrypt

## 📝 Licence

Projet privé - Tous droits réservés

## 👥 Auteurs

AGEN-OHADA Team
