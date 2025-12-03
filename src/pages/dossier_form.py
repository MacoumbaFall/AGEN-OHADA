import rio
from src.database import get_db
from src.models.dossier import Dossier
from datetime import datetime

class DossierFormPage(rio.Component):
    """
    Form for creating a new dossier
    """
    # Form fields
    intitule: str = ""
    type_dossier: str = "VENTE"
    error_message: str = ""
    success_message: str = ""
    
    # Callback to navigate back to list
    on_cancel: rio.EventHandler[[]] = None
    on_success: rio.EventHandler[[]] = None
    
    def generate_numero_dossier(self) -> str:
        """
        Generate automatic dossier number in format: YYYY-MM-SEQ
        Example: 2025-12-001
        """
        db = next(get_db())
        now = datetime.now()
        year_month = now.strftime("%Y-%m")
        
        # Count existing dossiers for this month
        count = db.query(Dossier).filter(
            Dossier.numero_dossier.like(f"{year_month}-%")
        ).count()
        
        # Generate sequential number
        seq = count + 1
        numero = f"{year_month}-{seq:03d}"
        
        return numero
    
    def on_submit(self):
        """Handle form submission"""
        # Validation
        if not self.intitule.strip():
            self.error_message = "L'intitulé du dossier est obligatoire"
            return
        
        try:
            db = next(get_db())
            
            # Generate numero
            numero = self.generate_numero_dossier()
            
            # Create new dossier
            new_dossier = Dossier(
                numero_dossier=numero,
                intitule=self.intitule.strip(),
                type_dossier=self.type_dossier,
                statut="OUVERT",
                date_ouverture=datetime.now().date(),
                responsable_id=1  # TODO: Use actual logged-in user ID
            )
            
            db.add(new_dossier)
            db.commit()
            
            self.success_message = f"Dossier {numero} créé avec succès !"
            self.error_message = ""
            
            # Clear form
            self.intitule = ""
            self.type_dossier = "VENTE"
            
            # Notify parent
            if self.on_success:
                self.on_success()
                
        except Exception as e:
            self.error_message = f"Erreur lors de la création : {str(e)}"
            db.rollback()
    
    def on_cancel_click(self):
        """Handle cancel button"""
        if self.on_cancel:
            self.on_cancel()
    
    def build(self) -> rio.Component:
        return rio.Column(
            rio.Text("Nouveau Dossier", style="heading1"),
            rio.Spacer(height=2),
            
            # Form
            rio.Card(
                rio.Column(
                    # Intitulé
                    rio.Text("Intitulé du dossier *", style="heading3"),
                    rio.TextInput(
                        text=self.bind().intitule,
                        label="Ex: Vente Immeuble Dakar",
                    ),
                    
                    rio.Spacer(height=1),
                    
                    # Type de dossier
                    rio.Text("Type de dossier", style="heading3"),
                    rio.Dropdown(
                        label="Sélectionner le type",
                        options=[
                            "VENTE",
                            "SUCCESSION",
                            "DONATION",
                            "CREDIT-BAIL",
                            "PROCURATION",
                            "TESTAMENT",
                            "CONSTITUTION_SOCIETE",
                            "AUTRE"
                        ],
                        selected_value=self.bind().type_dossier,
                    ),
                    
                    rio.Spacer(height=2),
                    
                    # Messages
                    rio.Text(
                        self.error_message,
                        style=rio.TextStyle(fill=rio.Color.RED)
                    ) if self.error_message else rio.Text(""),
                    
                    rio.Text(
                        self.success_message,
                        style=rio.TextStyle(fill=rio.Color.GREEN)
                    ) if self.success_message else rio.Text(""),
                    
                    rio.Spacer(height=1),
                    
                    # Buttons
                    rio.Row(
                        rio.Button(
                            "Annuler",
                            on_press=self.on_cancel_click,
                            style="minor"
                        ),
                        rio.Spacer(),
                        rio.Button(
                            "Créer le dossier",
                            icon="material/add",
                            on_press=self.on_submit,
                            style="major"
                        ),
                        spacing=2
                    ),
                    
                    spacing=1,
                    margin=2
                ),
                grow_x=True
            ),
            
            spacing=1,
            margin=2
        )
