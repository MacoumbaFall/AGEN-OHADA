from __future__ import annotations
import rio
from src.database import get_db
from src.models.dossier import Dossier
from datetime import datetime

class DossierListPage(rio.Component):
    """
    Page displaying the list of all dossiers with search and filters.
    """
    # Search and filter state
    search_query: str = ""
    filter_type: str = "TOUS"
    filter_statut: str = "TOUS"
    
    # Callbacks
    on_new_dossier: rio.EventHandler[[]] = None
    on_view_dossier: rio.EventHandler[[int]] = None
    
    def get_filtered_dossiers(self):
        """Fetch and filter dossiers based on search and filters"""
        db = next(get_db())
        query = db.query(Dossier)
        
        # Apply search filter
        if self.search_query.strip():
            search_term = f"%{self.search_query.strip()}%"
            query = query.filter(
                (Dossier.numero_dossier.like(search_term)) |
                (Dossier.intitule.like(search_term))
            )
        
        # Apply type filter
        if self.filter_type != "TOUS":
            query = query.filter(Dossier.type_dossier == self.filter_type)
        
        # Apply status filter
        if self.filter_statut != "TOUS":
            query = query.filter(Dossier.statut == self.filter_statut)
        
        # Order by date (most recent first)
        query = query.order_by(Dossier.date_ouverture.desc())
        
        return query.all()
    
    def on_dossier_click(self, dossier_id: int):
        """Handle dossier card click"""
        if self.on_view_dossier:
            self.on_view_dossier(dossier_id)
    
    def get_statut_color(self, statut: str) -> rio.Color:
        """Return color based on status"""
        colors = {
            "OUVERT": rio.Color.from_hex("3b82f6"),      # Blue
            "INSTRUCTION": rio.Color.from_hex("f59e0b"),  # Orange
            "SIGNATURE": rio.Color.from_hex("8b5cf6"),    # Purple
            "FORMALITES": rio.Color.from_hex("06b6d4"),   # Cyan
            "CLOTURE": rio.Color.from_hex("10b981"),      # Green
            "ARCHIVE": rio.Color.from_hex("6b7280"),      # Gray
        }
        return colors.get(statut, rio.Color.GREY)
    
    def build(self) -> rio.Component:
        # Debug print
        print(f"DEBUG: search_query value: {getattr(self, 'search_query', 'NOT_FOUND')}")

        # Fetch filtered dossiers
        dossiers = self.get_filtered_dossiers()
        
        # Create the list of dossier cards
        dossier_cards = []
        for dossier in dossiers:
            dossier_cards.append(
                rio.Card(
                    rio.Row(
                        # Left side - Main info
                        rio.Column(
                            rio.Text(dossier.intitule, style="heading3"),
                            rio.Row(
                                rio.Text(f"N° {dossier.numero_dossier}", style="text-dim"),
                                rio.Text("•", style="text-dim"),
                                rio.Text(dossier.type_dossier, style="text-dim"),
                                spacing=0.5
                            ),
                            spacing=0.5
                        ),
                        rio.Spacer(),
                        # Right side - Status and date
                        rio.Column(
                            rio.Card(
                                rio.Text(
                                    dossier.statut,
                                    style=rio.TextStyle(
                                        fill=rio.Color.WHITE,
                                        font_weight="bold",
                                        font_size=0.9
                                    )
                                ),
                                color=self.get_statut_color(dossier.statut),
                                margin=0.5
                            ),
                            rio.Text(
                                f"Ouvert le {dossier.date_ouverture.strftime('%d/%m/%Y')}" if dossier.date_ouverture else "Date inconnue",
                                style="text-dim"
                            ),
                            align_x=1,
                            spacing=0.5
                        ),
                        spacing=2,
                        align_y=0.5
                    ),
                    margin=0.5,
                    grow_x=True,
                    on_press=lambda dossier_id=dossier.id: self.on_dossier_click(dossier_id)
                )
            )
            
        # If no dossiers, show a message
        if not dossier_cards:
            content = rio.Column(
                rio.Icon("material/folder_off", fill=rio.Color.GREY, min_width=4, min_height=4),
                rio.Text(
                    "Aucun dossier trouvé" if not self.search_query else "Aucun résultat pour cette recherche",
                    style=rio.TextStyle(fill=rio.Color.GREY)
                ),
                align_x=0.5,
                spacing=1,
                margin_y=4
            )
        else:
            content = rio.Column(*dossier_cards, spacing=1)

        return rio.Column(
            # Header with title and new button
            rio.Row(
                rio.Text("Gestion des Dossiers", style="heading1"),
                rio.Spacer(),
                rio.Button(
                    "Nouveau Dossier", 
                    icon="material/add",
                    on_press=self.on_new_dossier if self.on_new_dossier else lambda: None,
                    style="major"
                ),
                spacing=2,
                align_y=0.5
            ),
            
            rio.Spacer(min_height=2),
            
            # Search and Filters
            rio.Card(
                rio.Column(
                    rio.Row(
                        # Search bar
                        rio.TextInput(
                            text=self.bind().search_query,
                            label="Rechercher par numéro ou intitulé...",
                            prefix_text="🔍",
                            grow_x=True
                        ),
                        # Type filter
                        rio.Dropdown(
                            label="Type",
                            options=[
                                "TOUS",
                                "VENTE",
                                "SUCCESSION",
                                "DONATION",
                                "CREDIT-BAIL",
                                "PROCURATION",
                                "TESTAMENT",
                                "CONSTITUTION_SOCIETE",
                                "AUTRE"
                            ],
                            selected_value=self.bind().filter_type,
                            min_width=15
                        ),
                        # Status filter
                        rio.Dropdown(
                            label="Statut",
                            options=[
                                "TOUS",
                                "OUVERT",
                                "INSTRUCTION",
                                "SIGNATURE",
                                "FORMALITES",
                                "CLOTURE",
                                "ARCHIVE"
                            ],
                            selected_value=self.bind().filter_statut,
                            min_width=15
                        ),
                        spacing=2
                    ),
                    margin=1
                ),
                grow_x=True
            ),
            
            rio.Spacer(min_height=1),
            
            # Results count
            rio.Text(
                f"{len(dossiers)} dossier(s) trouvé(s)",
                style="text-dim"
            ),
            
            rio.Spacer(min_height=1),
            
            # Dossiers list
            content,
            
            spacing=1,
            margin=2
        )
