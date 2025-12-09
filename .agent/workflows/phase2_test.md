---
description: Automated testing of Phase 2 (all test scenarios) using integrated browser
---

1. Start the application server
   ```bash
   cd "j:\\Mon Drive\\Projet AGEN-CdC"
   python -m src.main
   ```
   // turbo
2. Open the application in the integrated browser
   - URL: http://localhost:8000
   // turbo
3. Perform Test 1: Login
   - Fill username: `admin`
   - Fill password: `<your password>`
   - Click "Se connecter"
   - Verify redirection to dashboard
4. Perform Test 2: Navigate to Dossiers
   - Click sidebar "Dossiers"
   - Verify Dossiers page loads with search bar and filters
5. Perform Test 3: Create a new dossier
   - Click "Nouveau Dossier"
   - Fill form fields (Intitulé, Type, etc.)
   - Submit and verify success message and dossier appears in list
6. Perform Test 4: Search functionality
   - Use search bar with keyword "Vente"
   - Verify filtered results
7. Perform Test 5: Filter by type and status
   - Select type "VENTE" and status "OUVERT"
   - Verify filtered list
8. Perform Test 6: View dossier details
   - Click on a dossier card
   - Verify details page shows all information and action buttons
9. Perform Test 7: Edit dossier
   - Click "Modifier"
   - Change status to INSTRUCTION and update description, montant, émoluments, débours
   - Save and verify changes on details page
10. Perform Test 8: Change status to CLOTURE
    - Edit dossier, set status to CLOTURE, save
    - Verify closure date is set and badge color changes to green
11. Perform Test 9: Soft delete dossier
    - Click "Supprimer", confirm deletion
    - Verify dossier disappears from main list and appears under ARCHIVE filter
12. Perform Test 10: Restore archived dossier
    - Filter by ARCHIVE, select dossier, edit status back to OUVERT
    - Save and verify dossier returns to main list
13. Perform Test 11: Verify status badge colors
    - Ensure each status badge matches the specified color codes
14. Perform Test 12: Full navigation flow
    - Execute the complete navigation sequence from list → details → edit → back → create → cancel → etc.
    - Verify no errors occur throughout.

// turbo-all
