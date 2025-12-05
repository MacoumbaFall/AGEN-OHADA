import rio
from src.database import get_db
from src.models.dossier import Document
from datetime import datetime
import os
import shutil

class AddDocumentDialog(rio.Component):
    """
    Dialog to upload a new document to a dossier
    """
    dossier_id: int
    on_cancel: rio.EventHandler[[]] = None
    on_success: rio.EventHandler[[]] = None
    
    # Form fields
    titre: str = ""
    type_document: str = "PIECE_IDENTITE"
    file: rio.FileInfo = None
    
    error_message: str = ""
    is_loading: bool = False
    
    def on_file_upload(self, file: rio.FileInfo):
        self.file = file
        if not self.titre and file:
            # Auto-fill title with filename if empty
            self.titre = file.name
            
    def on_submit(self):
        if not self.titre:
            self.error_message = "Le titre est obligatoire"
            return
            
        if not self.file:
            self.error_message = "Veuillez sélectionner un fichier"
            return
            
        self.is_loading = True
        
        try:
            # Ensure uploads directory exists
            upload_dir = "uploads"
            if not os.path.exists(upload_dir):
                os.makedirs(upload_dir)
                
            # Generate unique filename
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{self.dossier_id}_{timestamp}_{self.file.name}"
            file_path = os.path.join(upload_dir, filename)
            
            # Save file
            with open(file_path, "wb") as f:
                f.write(self.file.read())
                
            # Save to database
            db = next(get_db())
            document = Document(
                dossier_id=self.dossier_id,
                titre=self.titre,
                type_document=self.type_document,
                chemin_fichier=file_path,
                taille_fichier=self.file.size,
                date_upload=datetime.utcnow()
            )
            
            db.add(document)
            db.commit()
            
            if self.on_success:
                self.on_success()
                
        except Exception as e:
            self.error_message = f"Erreur lors de l'upload : {str(e)}"
            # Try to cleanup file if db save failed
            if 'file_path' in locals() and os.path.exists(file_path):
                try:
                    os.remove(file_path)
                except:
                    pass
        finally:
            self.is_loading = False
            
    def build(self) -> rio.Component:
        return rio.Column(
            rio.Text("Ajouter un document", style="heading2"),
            
            rio.TextInput(
                label="Titre du document",
                text=self.bind().titre
            ),
            
            rio.Dropdown(
                label="Type de document",
                options=[
                    "PIECE_IDENTITE",
                    "TITRE_PROPRIETE",
                    "ACTE",
                    "CORRESPONDANCE",
                    "AUTRE"
                ],
                selected_value=self.bind().type_document
            ),
            
            rio.FilePicker(
                label="Choisir un fichier",
                on_choose=self.on_file_upload,
                file_types=["application/pdf", "image/*"]
            ),
            
            rio.Text(
                f"Fichier sélectionné : {self.file.name}" if self.file else "",
                style="text-dim"
            ),
            
            rio.Spacer(height=1),
            
            rio.Text(
                self.error_message,
                style=rio.TextStyle(fill=rio.Color.RED)
            ) if self.error_message else rio.Text(""),
            
            rio.Row(
                rio.Button(
                    "Annuler",
                    on_press=lambda: self.on_cancel() if self.on_cancel else None,
                    style="minor"
                ),
                rio.Spacer(),
                rio.Button(
                    "Uploader",
                    icon="material/upload",
                    on_press=self.on_submit,
                    is_loading=self.is_loading,
                    style="major"
                ),
                spacing=2
            ),
            spacing=1,
            margin=2,
            min_width=30
        )
