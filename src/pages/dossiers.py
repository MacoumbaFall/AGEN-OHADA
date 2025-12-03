import rio
from src.database import get_db
from src.models.dossier import Dossier
from datetime import datetime

class DossierListPage(rio.Component):
    """
    Page displaying the list of all dossiers.
    """
    # Callback for creating new dossier
    on_new_dossier: rio.EventHandler[[]] = None
    
    def build(self) -> rio.Component:
        # Fetch dossiers from database
        db = next(get_db())
        dossiers = db.query(Dossier).all()
        
        # Create the list of dossier cards
        dossier_cards = []
        for dossier in dossiers:
            dossier_cards.append(
                rio.Card(
                    rio.Row(
                        rio.Column(
                            rio.Text(dossier.intitule, style="heading3"),
                            rio.Text(f"N° {dossier.numero_dossier}", style="text-dim"),
                            spacing=0.5
                        ),
                        rio.Spacer(),
                        rio.Column(
                            rio.Text(dossier.statut, style=rio.TextStyle(font_weight="bold")),
                            rio.Text(f"Ouvert le {dossier.date_ouverture.strftime('%d/%m/%Y')}", style="text-dim"),
                            align_x=1,
                            spacing=0.5
                        ),
                        spacing=2,
                        align_y=0.5
                    ),
                    margin=0.5,
                    grow_x=True
                )
            )
            
        # If no dossiers, show a message
        if not dossier_cards:
            content = rio.Column(
                rio.Icon("material/folder_off", fill=rio.Color.GREY, min_width=4, min_height=4),
                rio.Text("Aucun dossier trouvé", style=rio.TextStyle(fill=rio.Color.GREY)),
                align_x=0.5,
                spacing=1
            )
        else:
            content = rio.Column(*dossier_cards, spacing=1)

        return rio.Column(
            rio.Row(
                rio.Text("Gestion des Dossiers", style="heading1"),
                rio.Spacer(),
                rio.Button(
                    "Nouveau Dossier", 
                    icon="material/add",
                    on_press=self.on_new_dossier if self.on_new_dossier else lambda: None
                ),
                spacing=2,
                align_y=0.5
            ),
            rio.Spacer(height=2),
            content,
            spacing=1,
            margin=2
        )
