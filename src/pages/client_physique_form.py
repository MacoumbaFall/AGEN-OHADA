import rio
from src.database import get_db
from src.models.client import Client
from datetime import datetime, date

class ClientPhysiqueForm(rio.Component):
    """
    Form for creating a new client (Personne Physique)
    """
    # Form fields
    nom: str = ""
    prenom: str = ""
    date_naissance: str = ""  # Format: YYYY-MM-DD
    lieu_naissance: str = ""
    adresse: str = ""
    telephone: str = ""
    email: str = ""
    identifiant_unique: str = ""  # NINA, CNI, etc.
    
    error_message: str = ""
    success_message: str = ""
    
    # Callbacks
    on_cancel: rio.EventHandler[[]] = None
    on_success: rio.EventHandler[[int]] = None  # Returns client_id
    
    def on_submit(self):
        """Handle form submission"""
        # Validation
        if not self.nom.strip():
            self.error_message = "Le nom est obligatoire"
            return
        
        if not self.prenom.strip():
            self.error_message = "Le prénom est obligatoire"
            return
        
        try:
            db = next(get_db())
            
            # Parse date if provided
            date_naissance_obj = None
            if self.date_naissance.strip():
                try:
                    date_naissance_obj = datetime.strptime(self.date_naissance, "%Y-%m-%d").date()
                except ValueError:
                    self.error_message = "Format de date invalide (utilisez AAAA-MM-JJ)"
                    return
            
            # Create new client
            new_client = Client(
                type_client="PHYSIQUE",
                nom=self.nom.strip(),
                prenom=self.prenom.strip(),
                date_naissance=date_naissance_obj,
                lieu_naissance=self.lieu_naissance.strip() if self.lieu_naissance else None,
                adresse=self.adresse.strip() if self.adresse else None,
                telephone=self.telephone.strip() if self.telephone else None,
                email=self.email.strip() if self.email else None,
                identifiant_unique=self.identifiant_unique.strip() if self.identifiant_unique else None
            )
            
            db.add(new_client)
            db.commit()
            db.refresh(new_client)
            
            self.success_message = f"Client {self.prenom} {self.nom} créé avec succès !"
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
            rio.Text("Nouveau Client - Personne Physique", style="heading2"),
            rio.Spacer(height=1),
            
            # Form
            rio.Card(
                rio.Column(
                    # Nom et Prénom
                    rio.Row(
                        rio.Column(
                            rio.Text("Nom *", style="heading3"),
                            rio.TextInput(
                                text=self.bind().nom,
                                label="Nom de famille",
                            ),
                            grow_x=True
                        ),
                        rio.Column(
                            rio.Text("Prénom *", style="heading3"),
                            rio.TextInput(
                                text=self.bind().prenom,
                                label="Prénom(s)",
                            ),
                            grow_x=True
                        ),
                        spacing=2
                    ),
                    
                    rio.Spacer(height=1),
                    
                    # Date et lieu de naissance
                    rio.Row(
                        rio.Column(
                            rio.Text("Date de naissance", style="heading3"),
                            rio.TextInput(
                                text=self.bind().date_naissance,
                                label="AAAA-MM-JJ",
                            ),
                            grow_x=True
                        ),
                        rio.Column(
                            rio.Text("Lieu de naissance", style="heading3"),
                            rio.TextInput(
                                text=self.bind().lieu_naissance,
                                label="Ville, Pays",
                            ),
                            grow_x=True
                        ),
                        spacing=2
                    ),
                    
                    rio.Spacer(height=1),
                    
                    # Adresse
                    rio.Text("Adresse", style="heading3"),
                    rio.TextInput(
                        text=self.bind().adresse,
                        label="Adresse complète",
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
                                label="email@example.com",
                            ),
                            grow_x=True
                        ),
                        spacing=2
                    ),
                    
                    rio.Spacer(height=1),
                    
                    # Identifiant unique
                    rio.Text("Identifiant unique (NINA, CNI, Passeport)", style="heading3"),
                    rio.TextInput(
                        text=self.bind().identifiant_unique,
                        label="Numéro d'identification",
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
                            "Créer le client",
                            icon="material/person_add",
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
