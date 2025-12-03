import rio
from src.database import get_db
from src.models.client import Client
from datetime import datetime

class ClientMoraleForm(rio.Component):
    """
    Form for creating a new client (Personne Morale)
    """
    # Form fields
    raison_sociale: str = ""
    forme_juridique: str = "SARL"
    date_creation: str = ""  # Format: YYYY-MM-DD
    siege_social: str = ""
    adresse: str = ""
    telephone: str = ""
    email: str = ""
    rccm: str = ""  # Registre du Commerce et du Crédit Mobilier
    ninea: str = ""  # Numéro d'Identification Nationale des Entreprises et Associations
    
    error_message: str = ""
    success_message: str = ""
    
    # Callbacks
    on_cancel: rio.EventHandler[[]] = None
    on_success: rio.EventHandler[[int]] = None  # Returns client_id
    
    def on_submit(self):
        """Handle form submission"""
        # Validation
        if not self.raison_sociale.strip():
            self.error_message = "La raison sociale est obligatoire"
            return
        
        try:
            db = next(get_db())
            
            # Parse date if provided
            date_creation_obj = None
            if self.date_creation.strip():
                try:
                    date_creation_obj = datetime.strptime(self.date_creation, "%Y-%m-%d").date()
                except ValueError:
                    self.error_message = "Format de date invalide (utilisez AAAA-MM-JJ)"
                    return
            
            # Build identifiant_unique from RCCM and NINEA
            identifiant_parts = []
            if self.rccm.strip():
                identifiant_parts.append(f"RCCM: {self.rccm.strip()}")
            if self.ninea.strip():
                identifiant_parts.append(f"NINEA: {self.ninea.strip()}")
            identifiant_unique = " | ".join(identifiant_parts) if identifiant_parts else None
            
            # Create new client
            new_client = Client(
                type_client="MORALE",
                nom=f"{self.raison_sociale.strip()} ({self.forme_juridique})",
                prenom=None,  # NULL for Personne Morale
                date_naissance=date_creation_obj,  # Date de création
                lieu_naissance=self.siege_social.strip() if self.siege_social else None,  # Siège social
                adresse=self.adresse.strip() if self.adresse else None,
                telephone=self.telephone.strip() if self.telephone else None,
                email=self.email.strip() if self.email else None,
                identifiant_unique=identifiant_unique
            )
            
            db.add(new_client)
            db.commit()
            db.refresh(new_client)
            
            self.success_message = f"Société {self.raison_sociale} créée avec succès !"
            self.error_message = ""
            
            # Notify parent with client_id
            if self.on_success:
                self.on_success(new_client.id)
                
        except Exception as e:
            self.error_message = f"Erreur lors de la création : {str(e)}"
            db.rollback()
    
    def on_cancel_click(self):
        """Handle cancel button"""
        if self.on_cancel:
            self.on_cancel()
    
    def build(self) -> rio.Component:
        return rio.Column(
            rio.Text("Nouveau Client - Personne Morale", style="heading2"),
            rio.Spacer(height=1),
            
            # Form
            rio.Card(
                rio.Column(
                    # Raison sociale et forme juridique
                    rio.Row(
                        rio.Column(
                            rio.Text("Raison sociale *", style="heading3"),
                            rio.TextInput(
                                text=self.bind().raison_sociale,
                                label="Nom de la société",
                            ),
                            grow_x=True
                        ),
                        rio.Column(
                            rio.Text("Forme juridique", style="heading3"),
                            rio.Dropdown(
                                label="Type de société",
                                options=[
                                    "SARL",
                                    "SA",
                                    "SAS",
                                    "SNC",
                                    "GIE",
                                    "ASSOCIATION",
                                    "ONG",
                                    "AUTRE"
                                ],
                                selected_value=self.bind().forme_juridique,
                            ),
                            min_width=15
                        ),
                        spacing=2
                    ),
                    
                    rio.Spacer(height=1),
                    
                    # Date de création et siège social
                    rio.Row(
                        rio.Column(
                            rio.Text("Date de création", style="heading3"),
                            rio.TextInput(
                                text=self.bind().date_creation,
                                label="AAAA-MM-JJ",
                            ),
                            grow_x=True
                        ),
                        rio.Column(
                            rio.Text("Siège social", style="heading3"),
                            rio.TextInput(
                                text=self.bind().siege_social,
                                label="Ville, Pays",
                            ),
                            grow_x=True
                        ),
                        spacing=2
                    ),
                    
                    rio.Spacer(height=1),
                    
                    # Adresse
                    rio.Text("Adresse complète", style="heading3"),
                    rio.TextInput(
                        text=self.bind().adresse,
                        label="Adresse du siège",
                        multiline=True,
                    ),
                    
                    rio.Spacer(height=1),
                    
                    # Contact
                    rio.Row(
                        rio.Column(
                            rio.Text("Téléphone", style="heading3"),
                            rio.TextInput(
                                text=self.bind().telephone,
                                label="+221 XX XXX XX XX",
                            ),
                            grow_x=True
                        ),
                        rio.Column(
                            rio.Text("Email", style="heading3"),
                            rio.TextInput(
                                text=self.bind().email,
                                label="contact@societe.com",
                            ),
                            grow_x=True
                        ),
                        spacing=2
                    ),
                    
                    rio.Spacer(height=1),
                    
                    # Identifiants
                    rio.Row(
                        rio.Column(
                            rio.Text("RCCM", style="heading3"),
                            rio.TextInput(
                                text=self.bind().rccm,
                                label="Numéro RCCM",
                            ),
                            grow_x=True
                        ),
                        rio.Column(
                            rio.Text("NINEA", style="heading3"),
                            rio.TextInput(
                                text=self.bind().ninea,
                                label="Numéro NINEA",
                            ),
                            grow_x=True
                        ),
                        spacing=2
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
                            "Créer la société",
                            icon="material/business",
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
            
            spacing=1
        )
