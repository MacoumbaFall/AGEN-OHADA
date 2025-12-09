import rio
from src.database import get_db
from src.models.template import Template
from datetime import datetime
from src.services.template_engine import TemplateEngine

class TemplateEditorPage(rio.Component):
    """
    Editor for creating or modifying a template.
    """
    template_id: int = None # If None, creating new
    on_save: rio.EventHandler[[]] = None
    on_cancel: rio.EventHandler[[]] = None
    
    # State
    titre: str = ""
    type_acte: str = "VENTE"
    contenu: str = ""
    description: str = ""
    
    error_message: str = ""
    engine: TemplateEngine = TemplateEngine()
    
    def on_mount(self):
        if self.template_id:
            self.load_template()
            
    def load_template(self):
        try:
            db = next(get_db())
            template = db.query(Template).filter(Template.id == self.template_id).first()
            if template:
                self.titre = template.titre
                self.type_acte = template.type_acte
                self.contenu = template.contenu
                self.description = template.description or ""
        except Exception as e:
            self.error_message = f"Erreur chargement: {str(e)}"

    def on_save_click(self):
        if not self.titre:
            self.error_message = "Le titre est requis"
            return
            
        try:
            db = next(get_db())
            
            if self.template_id:
                template = db.query(Template).filter(Template.id == self.template_id).first()
                if not template:
                    self.error_message = "Template introuvable"
                    return
            else:
                template = Template()
                db.add(template)
                
            template.titre = self.titre
            template.type_acte = self.type_acte
            template.contenu = self.contenu
            template.description = self.description
            template.updated_at = datetime.utcnow()
            
            db.commit()
            
            if self.on_save:
                self.on_save()
                
        except Exception as e:
            self.error_message = f"Erreur sauvegarde: {str(e)}"
            db.rollback()

    def insert_variable(self, var_name: str):
        self.contenu += f"{{{{ {var_name} }}}}"

    def build(self) -> rio.Component:
        available_vars = self.engine.get_available_variables()
        
        return rio.Column(
            rio.Text("Éditeur de Modèle", style="heading1"),
            
            rio.Row(
                rio.TextInput(label="Titre", text=self.bind().titre, grow_x=True),
                rio.Dropdown(
                    label="Type d'acte",
                    options=["VENTE", "PROCURATION", "BAIL", "AUTRE"],
                    selected_value=self.bind().type_acte
                ),
                spacing=2
            ),
            
            rio.TextInput(label="Description", text=self.bind().description),
            
            rio.Row(
                # Editor Area
                rio.Column(
                    rio.Text("Contenu (Jinja2 Template)", style="heading3"),
                    rio.TextInput(
                        text=self.bind().contenu, 
                        multiline=True, 
                        min_height=20,
                        grow_y=True
                    ),
                    grow_x=True,
                    grow_y=True
                ),
                
                # Sidebar with variables
                rio.Card(
                    rio.Column(
                        rio.Text("Variables Disponibles", style="heading3"),
                        rio.Text("Cliquez pour insérer", style="text-dim"),
                        rio.Spacer(height=1),
                        rio.Column(
                            *[
                                rio.Button(
                                    var, 
                                    style="minor", 
                                    on_press=lambda v=var: self.insert_variable(v)
                                ) for var in available_vars
                            ],
                            spacing=0.5,
                            scroll_y="auto",
                            max_height=30
                        ),
                        margin=1
                    ),
                    min_width=20
                ),
                spacing=2,
                grow_y=True
            ),
            
            # Actions
            rio.Row(
                rio.Button("Annuler", on_press=self.on_cancel, style="minor"),
                rio.Spacer(),
                rio.Button("Enregistrer", on_press=self.on_save_click, style="major"),
                spacing=2,
                margin_y=2
            ),
            spacing=1,
            margin=2,
            grow_y=True
        )
