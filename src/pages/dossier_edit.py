import rio
from src.database import get_db
from src.models.dossier import Dossier, DossierHistorique
from src.models.user import User
from datetime import datetime, date

class DossierEditPage(rio.Component):
    """
    Form for editing an existing dossier
    """
    dossier_id: int
    current_username: str = ""
    
    # Form fields
    intitule: str = ""
    type_dossier: str = "VENTE"
    statut: str = "OUVERT"
    description: str = ""
    montant_acte: str = ""
    emoluments: str = ""
    debours: str = ""
    
    error_message: str = ""
    success_message: str = ""
    is_loaded: bool = False
    
    # Callbacks
    on_cancel: rio.EventHandler[[]] = None
    on_success: rio.EventHandler[[int]] = None
    
    def on_mount(self):
        """Load dossier data when component mounts"""
        self.load_dossier()
    
    def load_dossier(self):
        """Fetch dossier from database and populate form"""
        try:
            db = next(get_db())
            dossier = db.query(Dossier).filter(Dossier.id == self.dossier_id).first()
            
            if not dossier:
                self.error_message = "Dossier non trouvé"
                return
            
            # Populate form fields
            self.intitule = dossier.intitule
            self.type_dossier = dossier.type_dossier
            self.statut = dossier.statut
            self.description = dossier.description or ""
            self.montant_acte = str(dossier.montant_acte) if dossier.montant_acte else ""
            self.emoluments = str(dossier.emoluments) if dossier.emoluments else ""
            self.debours = str(dossier.debours) if dossier.debours else ""
            
            self.is_loaded = True
            
        except Exception as e:
            self.error_message = f"Erreur lors du chargement : {str(e)}"
    
    def on_submit(self):
        """Handle form submission"""
        # Validation
        if not self.intitule.strip():
            self.error_message = "L'intitulé du dossier est obligatoire"
            return
        
        try:
            db = next(get_db())
            dossier = db.query(Dossier).filter(Dossier.id == self.dossier_id).first()
            
            if not dossier:
                self.error_message = "Dossier non trouvé"
                return
            
            # Update fields
            # Update fields
            dossier.intitule = self.intitule.strip()
            dossier.type_dossier = self.type_dossier
            
            # Check for status change
            if dossier.statut != self.statut:
                # Get current user
                user_id = None
                if self.current_username:
                    current_user = db.query(User).filter(User.username == self.current_username).first()
                    if current_user:
                        user_id = current_user.id

                # Create history record
                historique = DossierHistorique(
                    dossier_id=dossier.id,
                    ancien_statut=dossier.statut,
                    nouveau_statut=self.statut,
                    date_changement=datetime.utcnow(),
                    user_id=user_id,
                    commentaire="Changement de statut via modification dossier"
                )
                db.add(historique)
                
                # Update status
                dossier.statut = self.statut

            dossier.description = self.description.strip() if self.description else None
            
            # Update financial fields (with validation)
            try:
                dossier.montant_acte = float(self.montant_acte) if self.montant_acte else None
            except ValueError:
                self.error_message = "Montant de l'acte invalide"
                return
            
            try:
                dossier.emoluments = float(self.emoluments) if self.emoluments else None
            except ValueError:
                self.error_message = "Émoluments invalides"
                return
            
            try:
                dossier.debours = float(self.debours) if self.debours else None
            except ValueError:
                self.error_message = "Débours invalides"
                return
            
            # Update closure date if status is CLOTURE
            if self.statut == "CLOTURE" and not dossier.date_cloture:
                dossier.date_cloture = date.today()
            elif self.statut != "CLOTURE":
                dossier.date_cloture = None
            
            db.commit()
            
            self.success_message = f"Dossier {dossier.numero_dossier} modifié avec succès !"
            self.error_message = ""
            
            # Notify parent after a short delay
            if self.on_success:
                self.on_success(self.dossier_id)
                
        except Exception as e:
            self.error_message = f"Erreur lors de la modification : {str(e)}"
            db.rollback()
    
    def on_cancel_click(self):
        """Handle cancel button"""
        if self.on_cancel:
            self.on_cancel()
    
    def build(self) -> rio.Component:
        if not self.is_loaded and not self.error_message:
            return rio.Column(
                rio.Text("Chargement...", style="heading2"),
                align_x=0.5,
                align_y=0.5
            )
        
        if self.error_message and not self.is_loaded:
            return rio.Column(
                rio.Icon("material/error", fill=rio.Color.RED, min_width=4, min_height=4),
                rio.Text(self.error_message, style=rio.TextStyle(fill=rio.Color.RED)),
                rio.Button("Retour", on_press=self.on_cancel_click),
                align_x=0.5,
                align_y=0.5,
                spacing=2
            )
        
        return rio.Column(
            rio.Text("Modifier le Dossier", style="heading1"),
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
                    
                    rio.Spacer(height=1),
                    
                    # Statut
                    rio.Text("Statut", style="heading3"),
                    rio.Dropdown(
                        label="Sélectionner le statut",
                        options=[
                            "OUVERT",
                            "INSTRUCTION",
                            "SIGNATURE",
                            "FORMALITES",
                            "CLOTURE",
                            "ARCHIVE"
                        ],
                        selected_value=self.bind().statut,
                    ),
                    
                    rio.Spacer(height=1),
                    
                    # Description
                    rio.Text("Description", style="heading3"),
                    rio.TextInput(
                        text=self.bind().description,
                        label="Description détaillée du dossier",
                        multiline=True,
                    ),
                    
                    rio.Spacer(height=2),
                    
                    # Financial Information
                    rio.Text("Informations Financières", style="heading2"),
                    rio.Spacer(height=1),
                    
                    rio.Row(
                        rio.Column(
                            rio.Text("Montant de l'acte (FCFA)", style="heading3"),
                            rio.TextInput(
                                text=self.bind().montant_acte,
                                label="0",
                            ),
                            grow_x=True
                        ),
                        rio.Column(
                            rio.Text("Émoluments (FCFA)", style="heading3"),
                            rio.TextInput(
                                text=self.bind().emoluments,
                                label="0",
                            ),
                            grow_x=True
                        ),
                        rio.Column(
                            rio.Text("Débours (FCFA)", style="heading3"),
                            rio.TextInput(
                                text=self.bind().debours,
                                label="0",
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
                            "Enregistrer les modifications",
                            icon="material/save",
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
