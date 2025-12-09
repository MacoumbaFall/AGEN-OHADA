import rio
from src.database import get_db
from src.models.template import Template
from datetime import datetime

class TemplateListPage(rio.Component):
    """
    List of available templates.
    """
    # Event handlers
    on_edit_template: rio.EventHandler[[int]] = None
    on_create_template: rio.EventHandler[[]] = None
    
    def on_delete_click(self, template_id: int):
        # We might want a dialog here, but for now simple delete
        try:
            db = next(get_db())
            template = db.query(Template).filter(Template.id == template_id).first()
            if template:
                db.delete(template)
                db.commit()
                # Trigger rebuild/refresh
                self.force_refresh()
        except Exception as e:
            print(f"Error deleting template: {str(e)}")

    def build(self) -> rio.Component:
        db = next(get_db())
        templates = db.query(Template).all()
        
        rows = []
        for t in templates:
            rows.append(
                rio.Card(
                    rio.Row(
                        rio.Column(
                            rio.Text(t.titre, style="heading3"),
                            rio.Text(t.type_acte, style="text-dim"),
                            spacing=0.5
                        ),
                        rio.Spacer(),
                        rio.Button(
                            "Modifier",
                            icon="material/edit",
                            on_press=lambda id=t.id: self.on_edit_template(id) if self.on_edit_template else None,
                            style="minor"
                        ),
                        rio.Button(
                            "Supprimer",
                            icon="material/delete",
                            on_press=lambda id=t.id: self.on_delete_click(id),
                            style="danger"
                        ),
                        spacing=2,
                        align_y=0.5
                    ),
                    margin=0.5
                )
            )
            
        return rio.Column(
            rio.Row(
                rio.Text("Modèles d'actes", style="heading1"),
                rio.Spacer(),
                rio.Button(
                    "Nouveau Modèle",
                    icon="material/add",
                    on_press=self.on_create_template,
                    style="major"
                ),
                align_y=0.5,
                margin_y=2
            ),
            
            rio.Column(*rows, spacing=1) if rows else rio.Text("Aucun modèle défini."),
            
            spacing=1,
            margin=2
        )
