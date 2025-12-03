# Guide de Test - Module Dossiers CRUD

## 🚀 Démarrage de l'application

```bash
cd "j:\Mon Drive\Projet AGEN-CdC"
python -m src.main
```

L'application devrait s'ouvrir automatiquement dans votre navigateur à l'adresse : `http://localhost:8000`

---

## 🧪 Scénarios de test

### ✅ Test 1 : Connexion
1. Utilisez les identifiants de test :
   - **Username** : `admin` (ou autre utilisateur créé)
   - **Password** : (votre mot de passe)
2. Cliquez sur "Se connecter"
3. ✅ **Résultat attendu** : Redirection vers le tableau de bord

---

### ✅ Test 2 : Navigation vers Dossiers
1. Dans le menu latéral, cliquez sur **"Dossiers"**
2. ✅ **Résultat attendu** : 
   - Affichage de la page "Gestion des Dossiers"
   - Barre de recherche et filtres visibles
   - Message "Aucun dossier trouvé" si aucun dossier n'existe

---

### ✅ Test 3 : Création de dossiers
1. Cliquez sur **"Nouveau Dossier"**
2. Remplissez le formulaire :
   - **Intitulé** : "Vente Appartement Dakar Plateau"
   - **Type** : VENTE
3. Cliquez sur **"Créer le dossier"**
4. ✅ **Résultat attendu** :
   - Message de succès avec le numéro généré (ex: 2025-12-001)
   - Retour automatique à la liste
   - Le nouveau dossier apparaît dans la liste

**Répétez** ce test pour créer plusieurs dossiers :
- "Succession Famille Diop" (Type: SUCCESSION)
- "Procuration Voyage" (Type: PROCURATION)
- "Constitution SARL TechCorp" (Type: CONSTITUTION_SOCIETE)

---

### ✅ Test 4 : Recherche
1. Dans la barre de recherche, tapez : **"Vente"**
2. ✅ **Résultat attendu** : 
   - Seuls les dossiers contenant "Vente" dans l'intitulé ou le numéro s'affichent
   - Compteur de résultats mis à jour

3. Effacez la recherche
4. Tapez le numéro d'un dossier (ex: **"2025-12-001"**)
5. ✅ **Résultat attendu** : Seul ce dossier s'affiche

---

### ✅ Test 5 : Filtres
1. **Filtre par type** :
   - Sélectionnez "VENTE" dans le dropdown "Type"
   - ✅ **Résultat** : Seuls les dossiers de type VENTE s'affichent

2. **Filtre par statut** :
   - Sélectionnez "OUVERT" dans le dropdown "Statut"
   - ✅ **Résultat** : Seuls les dossiers ouverts s'affichent

3. **Combinaison** :
   - Recherche : "Vente"
   - Type : VENTE
   - Statut : OUVERT
   - ✅ **Résultat** : Filtrage combiné fonctionne

4. Remettez tout à "TOUS" pour voir tous les dossiers

---

### ✅ Test 6 : Consultation des détails
1. Cliquez sur **n'importe quelle carte de dossier**
2. ✅ **Résultat attendu** :
   - Navigation vers la page de détails
   - Affichage de toutes les informations :
     - Intitulé et numéro
     - Badge de statut coloré
     - Informations générales
     - Informations financières (vides pour l'instant)
     - Description
   - Boutons : Retour, Modifier, Supprimer

---

### ✅ Test 7 : Modification d'un dossier
1. Depuis la page de détails, cliquez sur **"Modifier"**
2. ✅ **Résultat attendu** : Formulaire pré-rempli avec les données actuelles

3. Modifiez les champs suivants :
   - **Statut** : INSTRUCTION
   - **Description** : "Dossier en cours d'instruction, documents en attente"
   - **Montant de l'acte** : 50000000
   - **Émoluments** : 2500000
   - **Débours** : 150000

4. Cliquez sur **"Enregistrer les modifications"**
5. ✅ **Résultat attendu** :
   - Message de succès
   - Retour à la page de détails
   - Toutes les modifications sont visibles

---

### ✅ Test 8 : Changement de statut vers CLOTURE
1. Modifiez un dossier
2. Changez le **Statut** vers **CLOTURE**
3. Enregistrez
4. ✅ **Résultat attendu** :
   - Date de clôture automatiquement définie (date du jour)
   - Badge de statut devient vert

5. Modifiez à nouveau et changez le statut vers **OUVERT**
6. ✅ **Résultat attendu** :
   - Date de clôture effacée (affiche "Non clôturé")

---

### ✅ Test 9 : Suppression (Soft Delete)
1. Depuis la page de détails, cliquez sur **"Supprimer"**
2. ✅ **Résultat attendu** :
   - Dialogue de confirmation s'affiche avec overlay
   - Icône d'avertissement orange
   - Message explicatif

3. Cliquez sur **"Annuler"**
4. ✅ **Résultat** : Dialogue se ferme, rien n'est supprimé

5. Cliquez à nouveau sur **"Supprimer"**
6. Cette fois, cliquez sur **"Confirmer la suppression"**
7. ✅ **Résultat attendu** :
   - Retour automatique à la liste
   - Le dossier n'apparaît plus dans la liste par défaut

8. Changez le filtre **Statut** vers **ARCHIVE**
9. ✅ **Résultat** : Le dossier supprimé apparaît avec statut ARCHIVE (badge gris)

---

### ✅ Test 10 : Restauration d'un dossier archivé
1. Avec le filtre Statut = ARCHIVE, cliquez sur un dossier archivé
2. Cliquez sur **"Modifier"**
3. Changez le **Statut** vers **OUVERT**
4. Enregistrez
5. ✅ **Résultat attendu** :
   - Le dossier est restauré
   - Il apparaît à nouveau dans la liste principale (filtre TOUS)

---

### ✅ Test 11 : Badges de statut colorés
Créez ou modifiez des dossiers pour avoir tous les statuts :
- 🔵 **OUVERT** : Bleu (#3b82f6)
- 🟠 **INSTRUCTION** : Orange (#f59e0b)
- 🟣 **SIGNATURE** : Violet (#8b5cf6)
- 🔷 **FORMALITES** : Cyan (#06b6d4)
- 🟢 **CLOTURE** : Vert (#10b981)
- ⚫ **ARCHIVE** : Gris (#6b7280)

✅ **Résultat attendu** : Chaque statut a sa couleur distinctive

---

### ✅ Test 12 : Navigation complète
Testez le flux complet :
1. **Liste** → Clic sur dossier → **Détails**
2. **Détails** → Modifier → **Édition**
3. **Édition** → Annuler → **Détails**
4. **Détails** → Retour → **Liste**
5. **Liste** → Nouveau Dossier → **Création**
6. **Création** → Annuler → **Liste**

✅ **Résultat attendu** : Navigation fluide sans erreur

---

## 🐛 Problèmes potentiels et solutions

### Problème : L'application ne démarre pas
**Solution** :
```bash
# Vérifier que l'environnement virtuel est activé
.venv\Scripts\activate

# Vérifier les dépendances
pip install -r requirements.txt
```

### Problème : Erreur de connexion à la base de données
**Solution** :
```bash
# Vérifier que PostgreSQL est démarré
# Vérifier les credentials dans .env
```

### Problème : Les dossiers ne s'affichent pas
**Solution** :
- Vérifier qu'il y a des dossiers dans la base de données
- Vérifier les filtres (remettre à TOUS)
- Vérifier la console pour les erreurs

---

## ✅ Checklist de validation

- [ ] Connexion fonctionne
- [ ] Création de dossier avec numérotation automatique
- [ ] Liste affiche tous les dossiers
- [ ] Recherche fonctionne (numéro et intitulé)
- [ ] Filtre par type fonctionne
- [ ] Filtre par statut fonctionne
- [ ] Clic sur dossier ouvre les détails
- [ ] Tous les champs sont affichés dans les détails
- [ ] Modification sauvegarde correctement
- [ ] Changement vers CLOTURE définit la date
- [ ] Suppression affiche le dialogue de confirmation
- [ ] Suppression archive le dossier (soft delete)
- [ ] Dossiers archivés visibles avec filtre ARCHIVE
- [ ] Restauration d'un dossier archivé fonctionne
- [ ] Badges de statut ont les bonnes couleurs
- [ ] Navigation entre pages fonctionne
- [ ] Boutons Annuler ramènent à la page précédente

---

## 📝 Notes de test

Utilisez cet espace pour noter vos observations :

```
Date du test : ___________
Testeur : ___________

Bugs trouvés :
- 
- 

Améliorations suggérées :
- 
- 

Commentaires :
- 
- 
```

---

**Bon test ! 🚀**
