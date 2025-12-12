---
description: Test automatisé de la création d'actes (Phase 3) via navigateur
---

# Test Phase 3 - Rédaction d'Actes

// turbo-all

1. Démarrer le serveur (si nécessaire)
   ```bash
   python -m src.main
   ```

2. Connexion
   - URL: http://localhost:8000
   - Login: `admin`
   - Password: `admin123`

3. Accéder à un dossier
   - Clic sur "Dossiers" (Sidebar)
   - Clic sur le premier dossier de la liste

4. Créer un nouvel acte
   - Clic sur l'onglet "Actes"
   - Clic sur "Rédiger un acte"
   - Champ Titre: "Ma Procuration Test"
   - Dropdown Modèle: "Procuration Générale"
   - Clic sur "Générer l'acte"

5. Vérifier et Enregistrer
   - Vérifier que le contenu a été généré (texte visible)
   - Dropdown Statut: "FINALISE"
   - Clic sur "Enregistrer"

6. Validation
   - Vérifier le retour à la liste des actes
   - Vérifier la présence de l'acte "Ma Procuration Test" en bleu/cyan
