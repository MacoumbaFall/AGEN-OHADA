import rio
from src.database import get_db
from src.models.client import Client
from src.models.dossier import DossierParties
from src.pages.client_physique_form import ClientPhysiqueForm
from src.pages.client_morale_form import ClientMoraleForm

class AddPartieDialog(rio.Component):
    """
    Dialog for adding a partie (client) to a dossier
    """
    dossier_id: int
    
    # State
    current_step: str = "select_mode"  # select_mode, select_client, create_physique, create_morale, select_role
    selected_client_id: int = None
    selected_role: str = "VENDEUR"
    search_query: str = ""
    
    error_message: str = ""
    success_message: str = ""
    
    # Callbacks
    on_cancel: rio.EventHandler[[]] = None
    on_success: rio.EventHandler[[]] = None
    
    def get_filtered_clients(self):
        """Get list of clients filtered by search"""
        db = next(get_db())
        query = db.query(Client)
        
        if self.search_query.strip():
            search_term = f"%{self.search_query.strip()}%"
            query = query.filter(
                (Client.nom.like(search_term)) |
                (Client.prenom.like(search_term)) |
                (Client.email.like(search_term))
            )
        
        return query.order_by(Client.nom).limit(50).all()
    
    def on_mode_select(self, mode: str):
        """Handle mode selection"""
        self.current_step = mode
        self.error_message = ""
    
    def on_client_select(self, client_id: int):
        """Handle client selection"""
        self.selected_client_id = client_id
        self.current_step = "select_role"
        self.error_message = ""
    
    def on_client_created(self, client_id: int):
        """Handle new client creation"""
        self.selected_client_id = client_id
        self.current_step = "select_role"
        self.error_message = ""
    
    def on_add_partie(self):
        """Add the partie to the dossier"""
        if not self.selected_client_id:
            self.error_message = "Aucun client sélectionné"
            return
        
        try:
            db = next(get_db())
            
            # Check if this client is already in this dossier
            existing = db.query(DossierParties).filter(
                DossierParties.dossier_id == self.dossier_id,
                DossierParties.client_id == self.selected_client_id
            ).first()
            
            if existing:
                self.error_message = "Ce client est déjà une partie de ce dossier"
                return
            
            # Create the association
            new_partie = DossierParties(
                dossier_id=self.dossier_id,
                client_id=self.selected_client_id,
                role_dans_acte=self.selected_role
            )
            
            db.add(new_partie)
            db.commit()
            
            self.success_message = "Partie ajoutée avec succès !"
            self.error_message = ""
            
            # Notify parent
            if self.on_success:
                self.on_success()
                
        except Exception as e:
            self.error_message = f"Erreur : {str(e)}"
            db.rollback()
    
    def on_cancel_click(self):
        """Handle cancel"""
        if self.on_cancel:
            self.on_cancel()
    
    def on_back(self):
        """Go back to previous step"""
        if self.current_step == "select_client":
            self.current_step = "select_mode"
        elif self.current_step in ["create_physique", "create_morale"]:
            self.current_step = "select_mode"
        elif self.current_step == "select_role":
            self.current_step = "select_mode"
        self.error_message = ""
    
    def build(self) -> rio.Component:
        # Step 1: Select mode
        if self.current_step == "select_mode":
            return self._build_mode_selection()
        
        # Step 2: Select existing client
        elif self.current_step == "select_client":
            return self._build_client_selection()
        
        # Step 3: Create new physique
        elif self.current_step == "create_physique":
            return rio.Column(
                rio.Button("← Retour", on_press=self.on_back, style="minor"),
                rio.Spacer(height=1),
                ClientPhysiqueForm(
                    on_cancel=self.on_back,
                    on_success=self.on_client_created
                ),
                spacing=1
            )
        
        # Step 4: Create new morale
        elif self.current_step == "create_morale":
            return rio.Column(
                rio.Button("← Retour", on_press=self.on_back, style="minor"),
                rio.Spacer(height=1),
                ClientMoraleForm(
                    on_cancel=self.on_back,
                    on_success=self.on_client_created
                ),
                spacing=1
            )
        
        # Step 5: Select role
        elif self.current_step == "select_role":
            return self._build_role_selection()
        
        return rio.Text("Erreur: État inconnu")
    
    def _build_mode_selection(self) -> rio.Component:
        """Build the mode selection view"""
        return rio.Column(
            rio.Text("Ajouter une partie au dossier", style="heading2"),
            rio.Spacer(height=2),
            
            rio.Card(
                rio.Column(
                    rio.Text("Choisissez une option :", style="heading3"),
                    rio.Spacer(height=1),
                    
                    rio.Button(
                        "Sélectionner un client existant",
                        icon="material/search",
                        on_press=lambda: self.on_mode_select("select_client"),
                        style="major",
                        min_width=30
                    ),
                    
                    rio.Spacer(height=1),
                    
                    rio.Button(
                        "Créer un nouveau client (Personne Physique)",
                        icon="material/person_add",
                        on_press=lambda: self.on_mode_select("create_physique"),
                        style="major",
                        min_width=30
                    ),
                    
                    rio.Spacer(height=1),
                    
                    rio.Button(
                        "Créer une nouvelle société (Personne Morale)",
                        icon="material/business",
                        on_press=lambda: self.on_mode_select("create_morale"),
                        style="major",
                        min_width=30
                    ),
                    
                    spacing=1,
                    margin=2,
                    align_x=0.5
                ),
                grow_x=True
            ),
            
            rio.Spacer(height=2),
            
            rio.Button(
                "Annuler",
                on_press=self.on_cancel_click,
                style="minor"
            ),
            
            spacing=1
        )
    
    def _build_client_selection(self) -> rio.Component:
        """Build the client selection view"""
        clients = self.get_filtered_clients()
        
        client_cards = []
        for client in clients:
            # Format display name
            if client.type_client == "PHYSIQUE":
                display_name = f"{client.prenom} {client.nom}"
                subtitle = f"Personne Physique"
            else:
                display_name = client.nom
                subtitle = "Personne Morale"
            
            client_cards.append(
                rio.Card(
                    rio.Row(
                        rio.Column(
                            rio.Text(display_name, style="heading3"),
                            rio.Text(subtitle, style="text-dim"),
                            rio.Text(f"📞 {client.telephone}" if client.telephone else "", style="text-dim"),
                            spacing=0.3
                        ),
                        rio.Spacer(),
                        rio.Button(
                            "Sélectionner",
                            on_press=lambda cid=client.id: self.on_client_select(cid),
                            style="major"
                        ),
                        spacing=2,
                        align_y=0.5
                    ),
                    margin=0.5
                )
            )
        
        return rio.Column(
            rio.Button("← Retour", on_press=self.on_back, style="minor"),
            rio.Spacer(height=1),
            
            rio.Text("Sélectionner un client", style="heading2"),
            rio.Spacer(height=1),
            
            # Search
            rio.TextInput(
                text=self.bind().search_query,
                label="Rechercher un client...",
                prefix_text="🔍"
            ),
            
            rio.Spacer(height=1),
            
            rio.Text(f"{len(clients)} client(s) trouvé(s)", style="text-dim"),
            
            rio.Spacer(height=1),
            
            # Client list
            rio.Column(*client_cards, spacing=1) if client_cards else rio.Text(
                "Aucun client trouvé",
                style=rio.TextStyle(fill=rio.Color.GREY)
            ),
            
            spacing=1
        )
    
    def _build_role_selection(self) -> rio.Component:
        """Build the role selection view"""
        return rio.Column(
            rio.Button("← Retour", on_press=self.on_back, style="minor"),
            rio.Spacer(height=1),
            
            rio.Text("Sélectionner le rôle", style="heading2"),
            rio.Spacer(height=2),
            
            rio.Card(
                rio.Column(
                    rio.Text("Rôle dans l'acte", style="heading3"),
                    rio.Dropdown(
                        label="Sélectionner le rôle",
                        options=[
                            "VENDEUR",
                            "ACQUEREUR",
                            "DONATEUR",
                            "DONATAIRE",
                            "TESTATEUR",
                            "HERITIER",
                            "MANDANT",
                            "MANDATAIRE",
                            "ASSOCIE",
                            "GERANT",
                            "AUTRE"
                        ],
                        selected_value=self.bind().selected_role,
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
                            "Ajouter la partie",
                            icon="material/add",
                            on_press=self.on_add_partie,
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
