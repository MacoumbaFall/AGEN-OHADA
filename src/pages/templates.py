from __future__ import annotations
import rio
from dataclasses import field
from src.database import SessionLocal
from src.models.template import Template
from sqlalchemy.exc import SQLAlchemyError

class TemplatesPage(rio.Component):
    """
    Page for managing document templates
    """
    # State
    templates: list[Template] = field(default_factory=list)
    selected_template_id: int = None
    is_editing: bool = False
    
    # Form State
    form_nom: str = ""
    form_type: str = "VENTE"
    form_description: str = ""
    form_contenu: str = ""
    error_message: str = ""
    success_message: str = ""
    
    def on_mount(self):
        self.load_templates()
        
    def load_templates(self):
        session = SessionLocal()
        try:
            self.templates = session.query(Template).order_by(Template.nom).all()
            # Detach objects so they can be used after session close if needed, 
            # though accessing lazy props will fail. 
            # Since Template has no relationships, this is fine.
            session.expunge_all() 
        except Exception as e:
            self.error_message = f"Erreur de chargement: {str(e)}"
        finally:
            session.close()

    def on_new_click(self):
        self.selected_template_id = None
        self.form_nom = ""
        self.form_type = "VENTE"
        self.form_description = ""
        self.form_contenu = ""
        self.is_editing = True
        self.error_message = ""
        self.success_message = ""

    def on_edit_click(self, template_id: int):
        self.selected_template_id = template_id
        session = SessionLocal()
        try:
            template = session.query(Template).filter(Template.id == template_id).first()
            if template:
                self.form_nom = template.nom
                self.form_type = template.type_acte
                self.form_description = template.description or ""
                self.form_contenu = template.contenu
                self.is_editing = True
                self.error_message = ""
                self.success_message = ""
        except Exception as e:
            self.error_message = f"Erreur: {str(e)}"
        finally:
            session.close()

    def on_cancel_edit(self):
        self.is_editing = False
        self.selected_template_id = None

    def on_save(self):
        if not self.form_nom:
            self.error_message = "Le nom est obligatoire"
            return
            
        if not self.form_contenu:
            self.error_message = "Le contenu est obligatoire"
            return

        session = SessionLocal()
        try:
            if self.selected_template_id:
                # Update
                template = session.query(Template).filter(Template.id == self.selected_template_id).first()
                if template:
                    template.nom = self.form_nom
                    template.type_acte = self.form_type
                    template.description = self.form_description
                    template.contenu = self.form_contenu
            else:
                # Create
                template = Template(
                    nom=self.form_nom,
                    type_acte=self.form_type,
                    description=self.form_description,
                    contenu=self.form_contenu
                )
                session.add(template)
            
            session.commit()
            self.is_editing = False
            self.success_message = "Template enregistré avec succès"
        except SQLAlchemyError as e:
            session.rollback()
            self.error_message = f"Erreur d'enregistrement: {str(e)}"
        except Exception as e:
            session.rollback()
            self.error_message = f"Erreur inattendue: {str(e)}"
        finally:
            session.close()
            # Reload templates to reflect changes
            self.load_templates()

    def on_delete_click(self, template_id: int):
        session = SessionLocal()
        try:
            template = session.query(Template).filter(Template.id == template_id).first()
            if template:
                session.delete(template)
                session.commit()
        except Exception as e:
            self.error_message = f"Erreur de suppression: {str(e)}"
        finally:
            session.close()
            self.load_templates()

    def build(self) -> rio.Component:
        if self.is_editing:
            return self._build_editor()
        return self._build_list()

    def _build_list(self) -> rio.Component:
        cards = []
        for t in self.templates:
            cards.append(
                rio.Card(
                    rio.Row(
                        rio.Column(
                            rio.Text(t.nom, style="heading3"),
                            rio.Text(f"{t.type_acte} - {t.description or ''}", style="text-dim"),
                            spacing=0.5
                        ),
                        rio.Spacer(),
                        rio.Button("Modifier", icon="material/edit", on_press=lambda id=t.id: self.on_edit_click(id), style="minor"),
                        rio.Button("Supprimer", icon="material/delete", on_press=lambda id=t.id: self.on_delete_click(id), style="minor"),
                        spacing=2,
                        align_y=0.5
                    ),
                    margin=0.5
                )
            )

        return rio.Column(
            rio.Row(
                rio.Text("Bibliothèque de Modèles", style="heading1"),
                rio.Spacer(),
                rio.Button("Nouveau Modèle", icon="material/add", on_press=self.on_new_click, style="major"),
                align_y=0.5
            ),
            rio.Spacer(height=2),
            rio.Column(*cards, spacing=1) if cards else rio.Text("Aucun modèle trouvé.", style="text-dim"),
            spacing=1,
            margin=2
        )

    def _build_editor(self) -> rio.Component:
        return rio.Column(
            rio.Text("Éditeur de Modèle", style="heading1"),
            rio.Spacer(height=2),
            
            rio.Row(
                rio.Column(
                    rio.TextInput(label="Nom du modèle", text=self.bind().form_nom),
                    rio.Dropdown(
                        label="Type d'Acte",
                        options=["VENTE", "PROCURATION", "TESTAMENT", "BAIL", "AUTRE"],
                        selected_value=self.bind().form_type
                    ),
                    rio.TextInput(label="Description", text=self.bind().form_description),
                    spacing=1,
                    grow_x=True
                ),
                rio.Card(
                    rio.Column(
                        rio.Text("Variables Disponibles", style="heading3"),
                        rio.Text("{{dossier.numero}}", style="text-dim"),
                        rio.Text("{{dossier.intitule}}", style="text-dim"),
                        rio.Text("{{client.nom}}", style="text-dim"),
                        rio.Text("{{client.prenom}}", style="text-dim"),
                        rio.Text("{{vendeur.nom}}", style="text-dim"),
                        rio.Text("{{acquereur.nom}}", style="text-dim"),
                        spacing=0.5
                    ),
                    margin=1,
                    min_width=20
                ),
                spacing=2
            ),
            
            rio.Spacer(height=1),
            rio.Text("Contenu du modèle", style="heading3"),
            rio.TextInput(
                text=self.bind().form_contenu,
                multiline=True,
                min_height=20
            ),
            
            rio.Spacer(height=2),
            rio.Row(
                rio.Button("Annuler", on_press=self.on_cancel_edit, style="minor"),
                rio.Spacer(),
                rio.Button("Enregistrer", icon="material/save", on_press=self.on_save, style="major"),
                spacing=2
            ),
            
            rio.Text(self.error_message, style=rio.TextStyle(fill=rio.Color.RED)) if self.error_message else rio.Text(""),
            
            spacing=1,
            margin=2
        )
