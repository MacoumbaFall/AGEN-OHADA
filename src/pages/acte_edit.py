from __future__ import annotations
import rio
from dataclasses import field
from src.database import SessionLocal
from src.models.acte import Acte, StatutActe
from src.models.dossier import Dossier
from src.models.template import Template
from src.utils.template_engine import TemplateEngine
from datetime import datetime

class ActeEditPage(rio.Component):
    """
    Page for creating or editing an Acte.
    """
    acte_id: int = None
    dossier_id: int = None # Required if creating new
    
    # Navigation callbacks
    on_cancel: rio.EventHandler[[]] = None
    on_success: rio.EventHandler[[]] = None
    
    # Internal State
    acte: Acte = None
    templates: list[Template] = field(default_factory=list)
    
    # Form State
    step: int = 1 # 1: Select Template/Metadata, 2: Edit Content
    form_titre: str = ""
    form_template_id: int = None
    form_contenu: str = ""
    form_statut: str = "BROUILLON"
    
    error_message: str = ""
    
    def __post_init__(self):
        """Load data immediately after component creation"""
        self.load_data()
    
    def on_mount(self):
        """Called when component is mounted - data already loaded in __post_init__"""
        pass
        
    def load_data(self):
        session = SessionLocal()
        try:
            # Load Templates for dropdown
            self.templates = session.query(Template).all()
            session.expunge_all()
            
            if self.acte_id:
                # Edit Mode
                acte = session.query(Acte).get(self.acte_id)
                if acte:
                    self.dossier_id = acte.dossier_id
                    self.form_titre = acte.titre
                    self.form_template_id = acte.template_id
                    self.form_contenu = acte.contenu
                    self.form_statut = acte.statut
                    self.step = 2 # Jump to editor directly
            elif self.dossier_id:
                # Create Mode
                dossier = session.query(Dossier).get(self.dossier_id)
                if dossier:
                    self.form_titre = f"Acte - {dossier.intitule}"
        except Exception as e:
            self.error_message = f"Erreur de chargement: {str(e)}"
        finally:
            session.close()

    def on_generate_click(self):
        """Generate content from template and move to editor"""
        if not self.form_template_id:
            self.error_message = "Veuillez sélectionner un modèle"
            return
            
        session = SessionLocal()
        try:
            template = session.query(Template).get(self.form_template_id)
            dossier = session.query(Dossier).get(self.dossier_id)
            
            if template and dossier:
                # Prepare Context
                # For now simple context, later we can enrich with parties info
                ctx = TemplateEngine.get_dossier_context(dossier)
                
                # Merge
                self.form_contenu = TemplateEngine.merge(template.contenu, ctx)
                
                # Clean up title if default
                if self.form_titre == f"Acte - {dossier.intitule}":
                     self.form_titre = f"{template.nom} - {dossier.numero_dossier}"
                
                self.step = 2
                self.error_message = ""
        except Exception as e:
            self.error_message = f"Erreur de génération: {str(e)}"
        finally:
            session.close()

    def on_save(self):
        if not self.form_titre:
            self.error_message = "Le titre est obligatoire"
            return
            
        session = SessionLocal()
        try:
            if self.acte_id:
                # Update
                acte = session.query(Acte).get(self.acte_id)
                acte.titre = self.form_titre
                acte.contenu = self.form_contenu
                acte.statut = self.form_statut
                # acte.template_id could be updated if we allow re-templating, but let's keep it simple
            else:
                # Create
                acte = Acte(
                    dossier_id=self.dossier_id,
                    template_id=self.form_template_id,
                    titre=self.form_titre,
                    contenu=self.form_contenu,
                    statut=self.form_statut
                )
                session.add(acte)
                
            session.commit()
            if self.on_success:
                self.on_success()
        except Exception as e:
            session.rollback()
            self.error_message = f"Erreur d'enregistrement: {str(e)}"
        finally:
            session.close()

    def build(self) -> rio.Component:
        if self.step == 1:
            return self._build_step1()
        else:
            return self._build_step2()

    def _build_step1(self) -> rio.Component:
        # Step 1: Selection du Template + Titre
        # Handle case where templates haven't loaded yet
        if not self.templates:
            template_options = {"Chargement...": 0}
        else:
            template_options = {t.nom: t.id for t in self.templates}
        
        return rio.Column(
            rio.Text("Nouvel Acte - Étape 1/2", style="heading1"),
            rio.Spacer(height=2),
            
            rio.Card(
                rio.Column(
                    rio.TextInput(label="Titre de l'acte", text=self.bind().form_titre),
                    rio.Dropdown(
                        label="Modèle (Template)",
                        options=template_options,
                        selected_value=self.bind().form_template_id
                    ),
                    rio.Spacer(height=1),
                    rio.Button(
                        "Générer l'acte", 
                        icon="material/article", 
                        on_press=self.on_generate_click, 
                        style="major",
                        is_sensitive=len(self.templates) > 0  # Disable if no templates
                    ),
                    spacing=1,
                    margin=2
                ),
                align_x=0.5,
                min_width=40
            ),
             rio.Spacer(height=2),
            rio.Button("Annuler", on_press=self.on_cancel, style="minor"),
             
            rio.Text(self.error_message, style=rio.TextStyle(fill=rio.Color.RED)) if self.error_message else rio.Text(""),
            align_x=0.5
        )

    def _build_step2(self) -> rio.Component:
        # Step 2: Édition du contenu
        return rio.Column(
            rio.Row(
                rio.Text("Éditeur d'Acte", style="heading1"),
                rio.Spacer(),
                rio.Dropdown(
                    options=["BROUILLON", "FINALISE", "SIGNE"],
                    selected_value=self.bind().form_statut
                ),
                rio.Button("Enregistrer", icon="material/save", on_press=self.on_save, style="major"),
                spacing=2,
                align_y=0.5
            ),
            rio.Spacer(height=1),
            
            rio.TextInput(label="Titre", text=self.bind().form_titre),
            rio.Spacer(height=1),
            
            rio.MultiLineTextInput(
                text=self.bind().form_contenu,
                grow_y=True,
                min_height=30
            ),
            
            rio.Spacer(height=1),
            rio.Button("Annuler", on_press=self.on_cancel, style="minor"),
            
            rio.Text(self.error_message, style=rio.TextStyle(fill=rio.Color.RED)) if self.error_message else rio.Text(""),
            grow_y=True,
            margin=2
        )
