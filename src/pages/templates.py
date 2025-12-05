import rio
from src.database import get_db
from src.models.template import Template
from datetime import datetime

class TemplatesPage(rio.Component):
    """
    Page for managing document templates
    """
    # State
    templates: list[Template] = []
    selected_template_id: int = None
    is_editing: bool = False
    
    # Form State
    form_titre: str = ""
    form_type: str = "VENTE"
    form_description: str = ""
    form_contenu: str = ""
    error_message: str = ""
    success_message: str = ""
    
    def on_mount(self):
        self.load_templates()
        
    def load_templates(self):
        try:
            db = next(get_db())
            self.templates = db.query(Template).order_by(Template.titre).all()
        except Exception as e:
            self.error_message = f"Erreur de chargement: {str(e)}"

    def on_new_click(self):
        self.selected_template_id = None
        self.form_titre = ""
        self.form_type = "VENTE"
        self.form_description = ""
        self.form_contenu = ""
        self.is_editing = True
        self.error_message = ""
        self.success_message = ""

    def on_edit_click(self, template_id: int):
        self.selected_template_id = template_id
        try:
            db = next(get_db())
            template = db.query(Template).filter(Template.id == template_id).first()
            if template:
                self.form_titre = template.titre
                self.form_type = template.type_acte
                self.form_description = template.description or ""
                self.form_contenu = template.contenu
                self.is_editing = True
                self.error_message = ""
                self.success_message = ""
        except Exception as e:
            self.error_message = f"Erreur: {str(e)}"

    def on_cancel_edit(self):
        self.is_editing = False
        self.selected_template_id = None

    def on_save(self):
        if not self.form_titre:
            self.error_message = "Le titre est obligatoire"
            return
            
        if not self.form_contenu:
            self.error_message = "Le contenu est obligatoire"
            return

        try:
            db = next(get_db())
            
            if self.selected_template_id:
                # Update
                template = db.query(Template).filter(Template.id == self.selected_template_id).first()
                if template:
                    template.titre = self.form_titre
                    template.type_acte = self.form_type
                    template.description = self.form_description
                    template.contenu = self.form_contenu
            else:
                # Create
                template = Template(
                    titre=self.form_titre,
                    type_acte=self.form_type,
                    description=self.form_description,
                    contenu=self.form_contenu
                )
                db.add(template)
            
            db.commit()
            self.load_templates()
            self.is_editing = False
            self.success_message = "Template enregistré avec succès"
            
        except Exception as e:
            self.error_message = f"Erreur d'enregistrement: {str(e)}"
            db.rollback()

    def on_delete_click(self, template_id: int):
        try:
            db = next(get_db())
            template = db.query(Template).filter(Template.id == template_id).first()
            if template:
                db.delete(template)
                db.commit()
                self.load_templates()
        except Exception as e:
            self.error_message = f"Erreur de suppression: {str(e)}"

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
                            rio.Text(t.titre, style="heading3"),
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
                    rio.TextInput(label="Titre", text=self.bind().form_titre),
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
