from __future__ import annotations
import rio
from src.database import get_db
from src.models.dossier import Dossier, DossierParties, DossierHistorique, Document
from src.models.acte import Acte
from src.models.user import User
from src.models.client import Client
from src.pages.add_partie_dialog import AddPartieDialog
from src.pages.add_document_dialog import AddDocumentDialog
from datetime import datetime
import os

class DossierDetailPage(rio.Component):
    """
    Detailed view of a single dossier with all information
    """
    dossier_id: int
    dossier: Dossier = None
    error_message: str = ""
    current_tab: str = "actes"  # parties, documents, historique, actes
    show_add_partie_dialog: bool = False
    partie_to_delete: tuple = None  # (dossier_id, client_id)
    show_delete_partie_dialog: bool = False
    
    # GED State
    show_add_document_dialog: bool = False
    document_to_delete_id: int = None
    show_delete_document_dialog: bool = False
    
    # Callbacks
    on_back: rio.EventHandler[[]] = None
    on_edit: rio.EventHandler[[int]] = None
    on_delete: rio.EventHandler[[int]] = None
    on_new_acte: rio.EventHandler[[]] = None
    on_edit_acte: rio.EventHandler[[int]] = None
    
    @rio.event.on_mount
    def on_mount(self):
        """Load dossier data when component mounts"""
        self.load_dossier()
    
    def load_dossier(self):
        """Fetch dossier from database"""
        db = None
        try:
            db = next(get_db())
            # Eagerly load the dossier with all relationships to avoid lazy-loading issues
            from sqlalchemy.orm import joinedload
            
            dossier = db.query(Dossier).options(
                joinedload(Dossier.responsable),
                joinedload(Dossier.parties_associations).joinedload(DossierParties.client),
                joinedload(Dossier.historique).joinedload(DossierHistorique.user),
                joinedload(Dossier.documents),
                joinedload(Dossier.actes)
            ).filter(Dossier.id == self.dossier_id).first()
            
            if not dossier:
                self.error_message = "Dossier non trouvé"
                print(f"[ERROR] Dossier with ID {self.dossier_id} not found")
                return
            
            # Detach from session to make it accessible after session closes
            db.expunge(dossier)
            self.dossier = dossier
            print(f"[INFO] Dossier {dossier.numero_dossier} loaded successfully")
            
        except Exception as e:
            self.error_message = f"Erreur lors du chargement : {str(e)}"
            print(f"[ERROR] Error loading dossier: {str(e)}")
            import traceback
            traceback.print_exc()
        finally:
            if db:
                db.close()
    
    def on_back_click(self):
        """Handle back button"""
        if self.on_back:
            self.on_back()
    
    def on_edit_click(self):
        """Handle edit button"""
        if self.on_edit:
            self.on_edit(self.dossier_id)
    
    def on_delete_click(self):
        """Handle delete button"""
        if self.on_delete:
            self.on_delete(self.dossier_id)
    
    def on_tab_change(self, tab: str):
        """Handle tab change"""
        self.current_tab = tab
    
    def on_add_partie_click(self):
        """Show add partie dialog"""
        self.show_add_partie_dialog = True
    
    def on_add_partie_success(self):
        """Handle successful partie addition"""
        self.show_add_partie_dialog = False
        self.load_dossier()  # Reload to show new partie
    
    def on_add_partie_cancel(self):
        """Handle partie dialog cancel"""
        self.show_add_partie_dialog = False
    
    def on_remove_partie_request(self, dossier_id: int, client_id: int):
        """Request to remove a partie"""
        self.partie_to_delete = (dossier_id, client_id)
        self.show_delete_partie_dialog = True
    
    def on_remove_partie_confirm(self):
        """Confirm and remove partie"""
        if not self.partie_to_delete:
            return
        
        try:
            db = next(get_db())
            dossier_id, client_id = self.partie_to_delete
            
            partie = db.query(DossierParties).filter(
                DossierParties.dossier_id == dossier_id,
                DossierParties.client_id == client_id
            ).first()
            
            if partie:
                db.delete(partie)
                db.commit()
                self.load_dossier()  # Reload
            
        except Exception as e:
            print(f"Error removing partie: {str(e)}")
            db.rollback()
        finally:
            self.show_delete_partie_dialog = False
            self.partie_to_delete = None
    
    def on_remove_partie_cancel(self):
        """Cancel partie removal"""
        self.show_delete_partie_dialog = False
        self.partie_to_delete = None

    # GED Handlers
    def on_add_document_click(self):
        self.show_add_document_dialog = True
        
    def on_add_document_success(self):
        self.show_add_document_dialog = False
        self.load_dossier()
        
    def on_add_document_cancel(self):
        self.show_add_document_dialog = False
        
    def on_delete_document_request(self, doc_id: int):
        self.document_to_delete_id = doc_id
        self.show_delete_document_dialog = True
        
    def on_delete_document_confirm(self):
        if not self.document_to_delete_id:
            return
            
        try:
            db = next(get_db())
            document = db.query(Document).filter(Document.id == self.document_to_delete_id).first()
            
            if document:
                # Remove file from disk
                import os
                if os.path.exists(document.chemin_fichier):
                    try:
                        os.remove(document.chemin_fichier)
                    except:
                        pass
                
                # Remove from db
                db.delete(document)
                db.commit()
                self.load_dossier()
                
        except Exception as e:
            print(f"Error deleting document: {str(e)}")
            db.rollback()
        finally:
            self.show_delete_document_dialog = False
            self.document_to_delete_id = None
            
    def on_delete_document_cancel(self):
        self.show_delete_document_dialog = False
        self.document_to_delete_id = None
    
    def get_statut_color(self, statut: str) -> rio.Color:
        """Return color based on status"""
        colors = {
            "OUVERT": rio.Color.from_hex("3b82f6"),
            "INSTRUCTION": rio.Color.from_hex("f59e0b"),
            "SIGNATURE": rio.Color.from_hex("8b5cf6"),
            "FORMALITES": rio.Color.from_hex("06b6d4"),
            "CLOTURE": rio.Color.from_hex("10b981"),
            "ARCHIVE": rio.Color.from_hex("6b7280"),
        }
        return colors.get(statut, rio.Color.GREY)
    
    def build(self) -> rio.Component:
        # Show error if dossier not found
        if self.error_message:
            return rio.Column(
                rio.Icon("material/error", fill=rio.Color.RED, min_width=4, min_height=4),
                rio.Text(self.error_message, style=rio.TextStyle(fill=rio.Color.RED, font_size=1.2)),
                rio.Button("Retour", icon="material/arrow_back", on_press=self.on_back_click),
                align_x=0.5,
                align_y=0.5,
                spacing=2
            )
        
        if not self.dossier:
            return rio.Column(
                rio.Text("Chargement...", style="heading2"),
                align_x=0.5,
                align_y=0.5
            )
        
        # Build main content
        main_content = rio.Column(
            # Header with actions
            rio.Row(
                rio.Button(
                    "Retour",
                    icon="material/arrow_back",
                    on_press=self.on_back_click,
                    style="minor"
                ),
                rio.Spacer(),
                rio.Button(
                    "Modifier",
                    icon="material/edit",
                    on_press=self.on_edit_click,
                    style="major"
                ),
                rio.Button(
                    "Supprimer",
                    icon="material/delete",
                    on_press=self.on_delete_click,
                    style="minor"
                ),
                spacing=1,
                align_y=0.5
            ),
            
            rio.Spacer(height=2),
            
            # Title and Status
            rio.Row(
                rio.Column(
                    rio.Text(self.dossier.intitule, style="heading1"),
                    rio.Text(f"N° {self.dossier.numero_dossier}", style="text-dim"),
                    spacing=0.5
                ),
                rio.Spacer(),
                rio.Card(
                    rio.Text(
                        self.dossier.statut,
                        style=rio.TextStyle(
                            fill=rio.Color.WHITE,
                            font_weight="bold"
                        )
                    ),
                    color=self.get_statut_color(self.dossier.statut),
                    margin=1
                ),
                spacing=2,
                align_y=0.5
            ),
            
            rio.Spacer(height=2),
            
            # Information Cards
            rio.Row(
                # General Information
                rio.Card(
                    rio.Column(
                        rio.Text("Informations Générales", style="heading2"),
                        rio.Spacer(height=1),
                        
                        self._info_row("Type de dossier", self.dossier.type_dossier),
                        self._info_row("Date d'ouverture", self.dossier.date_ouverture.strftime("%d/%m/%Y") if self.dossier.date_ouverture else "N/A"),
                        self._info_row("Date de clôture", self.dossier.date_cloture.strftime("%d/%m/%Y") if self.dossier.date_cloture else "Non clôturé"),
                        self._info_row("Responsable", f"User #{self.dossier.responsable_id}"),
                        
                        spacing=1,
                        margin=2
                    ),
                    grow_x=True
                ),
                
                # Financial Information
                rio.Card(
                    rio.Column(
                        rio.Text("Informations Financières", style="heading2"),
                        rio.Spacer(height=1),
                        
                        self._info_row("Montant de l'acte", f"{self.dossier.montant_acte:,.0f} FCFA" if self.dossier.montant_acte else "N/A"),
                        self._info_row("Émoluments", f"{self.dossier.emoluments:,.0f} FCFA" if self.dossier.emoluments else "N/A"),
                        self._info_row("Débours", f"{self.dossier.debours:,.0f} FCFA" if self.dossier.debours else "N/A"),
                        self._info_row("Total honoraires", f"{(self.dossier.emoluments or 0) + (self.dossier.debours or 0):,.0f} FCFA"),
                        
                        spacing=1,
                        margin=2
                    ),
                    grow_x=True
                ),
                spacing=2
            ),
            
            rio.Spacer(height=2),
            
            # Description
            rio.Card(
                rio.Column(
                    rio.Text("Description", style="heading2"),
                    rio.Spacer(height=1),
                    rio.Text(
                        self.dossier.description if self.dossier.description else "Aucune description",
                        style=rio.TextStyle(fill=rio.Color.GREY if not self.dossier.description else None)
                    ),
                    spacing=1,
                    margin=2
                ),
                grow_x=True
            ),
            
            rio.Spacer(height=2),
            
            # Tabs
            rio.Card(
                rio.Column(
                    rio.Row(
                        rio.Button(
                            "Parties",
                            style="major" if self.current_tab == "parties" else "minor",
                            on_press=lambda: self.on_tab_change("parties")
                        ),
                        rio.Button(
                            "Documents",
                            style="major" if self.current_tab == "documents" else "minor",
                            on_press=lambda: self.on_tab_change("documents")
                        ),
                        rio.Button(
                            "Actes",
                            style="major" if self.current_tab == "actes" else "minor",
                            on_press=lambda: self.on_tab_change("actes")
                        ),
                        rio.Button(
                            "Historique",
                            style="major" if self.current_tab == "historique" else "minor",
                            on_press=lambda: self.on_tab_change("historique")
                        ),
                        spacing=1
                    ),
                    rio.Spacer(height=2),
                    
                    # Tab content
                    self._build_tab_content(),
                    
                    spacing=1,
                    margin=2
                ),
                grow_x=True
            ),
            
            spacing=1,
            margin=2
        )
        
        # Overlay add partie dialog if needed
        if self.show_add_partie_dialog:
            main_content = rio.Overlay(
                rio.Card(
                    AddPartieDialog(
                        dossier_id=self.dossier_id,
                        on_cancel=self.on_add_partie_cancel,
                        on_success=self.on_add_partie_success
                    ),
                    color=rio.Color.WHITE,
                    min_width=40,
                    align_x=0.5,
                    align_y=0.5
                )
            )
        
        # Overlay delete partie confirmation if needed
        if self.show_delete_partie_dialog:
            main_content = rio.Overlay(
                rio.Card(
                    rio.Column(
                        rio.Icon("material/warning", fill=rio.Color.from_hex("f59e0b"), min_width=4, min_height=4),
                        rio.Text("Retirer cette partie ?", style="heading2"),
                        rio.Text(
                            "Êtes-vous sûr de vouloir retirer cette partie du dossier ?",
                            style="text-dim"
                        ),
                        rio.Spacer(height=2),
                        rio.Row(
                            rio.Button(
                                "Annuler",
                                on_press=self.on_remove_partie_cancel,
                                style="minor"
                            ),
                            rio.Spacer(),
                            rio.Button(
                                "Confirmer",
                                icon="material/delete",
                                on_press=self.on_remove_partie_confirm,
                                style="major"
                            ),
                            spacing=2
                        ),
                        spacing=1,
                        margin=2,
                        align_x=0.5
                    ),
                    color=rio.Color.WHITE,
                    min_width=30,
                    align_x=0.5,
                    align_y=0.5
                )
            )
        
        # Overlay add document dialog
        if self.show_add_document_dialog:
            main_content = rio.Overlay(
                rio.Card(
                    AddDocumentDialog(
                        dossier_id=self.dossier_id,
                        on_cancel=self.on_add_document_cancel,
                        on_success=self.on_add_document_success
                    ),
                    color=rio.Color.WHITE,
                    min_width=40,
                    align_x=0.5,
                    align_y=0.5
                )
            )
            
        # Overlay delete document confirmation
        if self.show_delete_document_dialog:
            main_content = rio.Overlay(
                rio.Card(
                    rio.Column(
                        rio.Icon("material/warning", fill=rio.Color.from_hex("f59e0b"), min_width=4, min_height=4),
                        rio.Text("Supprimer ce document ?", style="heading2"),
                        rio.Text(
                            "Cette action est irréversible. Le fichier sera supprimé du disque.",
                            style="text-dim"
                        ),
                        rio.Spacer(height=2),
                        rio.Row(
                            rio.Button(
                                "Annuler",
                                on_press=self.on_delete_document_cancel,
                                style="minor"
                            ),
                            rio.Spacer(),
                            rio.Button(
                                "Confirmer",
                                icon="material/delete",
                                on_press=self.on_delete_document_confirm,
                                style="major"
                            ),
                            spacing=2
                        ),
                        spacing=1,
                        margin=2,
                        align_x=0.5
                    ),
                    color=rio.Color.WHITE,
                    min_width=30,
                    align_x=0.5,
                    align_y=0.5
                )
            )
        
        return main_content
    
    def _build_tab_content(self) -> rio.Component:
        """Build content for the current tab"""
        if self.current_tab == "parties":
            return self._build_parties_tab()
        elif self.current_tab == "documents":
            return self._build_documents_tab()
        elif self.current_tab == "historique":
            return self._build_historique_tab()
        elif self.current_tab == "actes":
            return self._build_actes_tab()
        return rio.Text("")
    
    def _build_documents_tab(self) -> rio.Component:
        """Build the documents tab content"""
        # Use the eagerly-loaded documents from the dossier
        documents = self.dossier.documents if self.dossier else []
        
        doc_cards = []
        for doc in documents:
            icon = "material/description"
            if "pdf" in doc.chemin_fichier.lower():
                icon = "material/picture_as_pdf"
            elif "image" in doc.type_document.lower():
                icon = "material/image"
                
            doc_cards.append(
                rio.Card(
                    rio.Row(
                        rio.Icon(icon, fill=rio.Color.from_hex("3b82f6")),
                        rio.Column(
                            rio.Text(doc.titre, style="heading3"),
                            rio.Text(f"{doc.type_document} - {doc.date_upload.strftime('%d/%m/%Y')}", style="text-dim"),
                            spacing=0.3
                        ),
                        rio.Spacer(),
                        rio.Button(
                            "Ouvrir",
                            icon="material/visibility",
                            # Open file with default system viewer
                            on_press=lambda path=doc.chemin_fichier: os.startfile(path) if os.path.exists(path) else print(f"File not found: {path}"), 
                            style="minor"
                        ),
                        rio.Button(
                            "Supprimer",
                            icon="material/delete",
                            on_press=lambda d=doc.id: self.on_delete_document_request(d),
                            style="minor"
                        ),
                        spacing=2,
                        align_y=0.5
                    ),
                    margin=0.5
                )
            )
            
        return rio.Column(
            rio.Row(
                rio.Text(f"{len(documents)} document(s)", style="heading3"),
                rio.Spacer(),
                rio.Button(
                    "Ajouter un document",
                    icon="material/upload_file",
                    on_press=self.on_add_document_click,
                    style="major"
                ),
                spacing=2,
                align_y=0.5
            ),
            
            rio.Spacer(height=1),
            
            rio.Column(*doc_cards, spacing=1) if doc_cards else rio.Column(
                rio.Icon("material/folder_open", fill=rio.Color.GREY, min_width=3, min_height=3),
                rio.Text("Aucun document", style=rio.TextStyle(fill=rio.Color.GREY)),
                align_x=0.5,
                spacing=1,
                margin_y=2
            ),
            
            spacing=1
        )

    def _build_historique_tab(self) -> rio.Component:
        """Build the history tab content"""
        # Use the eagerly-loaded history from the dossier
        history = sorted(
            self.dossier.historique if self.dossier else [],
            key=lambda x: x.date_changement,
            reverse=True
        )
        
        history_items = []
        for item in history:
            history_items.append(
                rio.Card(
                    rio.Row(
                        rio.Column(
                            rio.Text(
                                item.date_changement.strftime("%d/%m/%Y %H:%M"),
                                style="text-dim"
                            ),
                            rio.Text(
                                f"Statut modifié : {item.ancien_statut} ➔ {item.nouveau_statut}",
                                style=rio.TextStyle(font_weight="bold")
                            ),
                            rio.Text(f"Par : {item.user.username}" if item.user else "Par : Inconnu", style="text-dim"),
                            rio.Text(item.commentaire or "", style="text-dim"),
                            spacing=0.5
                        ),
                        rio.Spacer(),
                        rio.Icon("material/history", fill=rio.Color.GREY),
                        spacing=2,
                        align_y=0.5
                    ),
                    margin=0.5
                )
            )
            
        return rio.Column(
            rio.Text("Historique des changements", style="heading3"),
            rio.Spacer(height=1),
            
            rio.Column(*history_items, spacing=1) if history_items else rio.Column(
                rio.Icon("material/history_toggle_off", fill=rio.Color.GREY, min_width=3, min_height=3),
                rio.Text("Aucun historique disponible", style=rio.TextStyle(fill=rio.Color.GREY)),
                align_x=0.5,
                spacing=1,
                margin_y=2
            ),
            
            spacing=1
        )
    
    def _build_parties_tab(self) -> rio.Component:
        """Build the parties tab content"""
        # Use the eagerly-loaded parties from the dossier
        parties_associations = self.dossier.parties_associations if self.dossier else []
        
        
        partie_cards = []
        for partie_assoc in parties_associations:
            client = partie_assoc.client
            # Format client name
            if client.type_client == "PHYSIQUE":
                client_name = f"{client.prenom} {client.nom}"
                client_type = "👤 Personne Physique"
            else:
                client_name = client.nom
                client_type = "🏢 Personne Morale"
            
            partie_cards.append(
                rio.Card(
                    rio.Row(
                        rio.Column(
                            rio.Text(client_name, style="heading3"),
                            rio.Text(client_type, style="text-dim"),
                            rio.Text(f"📞 {client.telephone}" if client.telephone else "", style="text-dim"),
                            spacing=0.3
                        ),
                        rio.Spacer(),
                        rio.Column(
                            rio.Card(
                                rio.Text(
                                    partie_assoc.role_dans_acte,
                                    style=rio.TextStyle(
                                        fill=rio.Color.WHITE,
                                        font_weight="bold",
                                        font_size=0.9
                                    )
                                ),
                                color=rio.Color.from_hex("3b82f6"),
                                margin=0.5
                            ),
                            rio.Button(
                                "Retirer",
                                icon="material/remove",
                                on_press=lambda did=self.dossier_id, cid=client.id: self.on_remove_partie_request(did, cid),
                                style="minor"
                            ),
                            spacing=0.5,
                            align_x=1
                        ),
                        spacing=2,
                        align_y=0.5
                    ),
                    margin=0.5
                )
            )
        
        return rio.Column(
            rio.Row(
                rio.Text(f"{len(parties_associations)} partie(s)", style="heading3"),
                rio.Spacer(),
                rio.Button(
                    "Ajouter une partie",
                    icon="material/person_add",
                    on_press=self.on_add_partie_click,
                    style="major"
                ),
                spacing=2,
                align_y=0.5
            ),
            
            rio.Spacer(height=1),
            
            rio.Column(*partie_cards, spacing=1) if partie_cards else rio.Column(
                rio.Icon("material/group_off", fill=rio.Color.GREY, min_width=3, min_height=3),
                rio.Text("Aucune partie ajoutée", style=rio.TextStyle(fill=rio.Color.GREY)),
                align_x=0.5,
                spacing=1,
                margin_y=2
            ),
            
            spacing=1
        )
    
    def _build_actes_tab(self) -> rio.Component:
        """Build the actes tab content"""
        # Use the eagerly-loaded actes from the dossier
        actes = sorted(
            self.dossier.actes if self.dossier else [],
            key=lambda x: x.created_at,
            reverse=True
        )
        
        acte_cards = []
        for acte in actes:
            status_color = rio.Color.GREY
            if acte.statut == "FINALISE":
                status_color = rio.Color.from_hex("06b6d4")
            elif acte.statut == "SIGNE":
                status_color = rio.Color.from_hex("10b981")
            else: # BROUILLON
                status_color = rio.Color.from_hex("f59e0b")

            acte_cards.append(
                rio.Card(
                    rio.Row(
                        rio.Icon("material/gavel", fill=status_color),
                        rio.Column(
                            rio.Text(acte.titre, style="heading3"),
                            rio.Text(f"{acte.statut}", style=rio.TextStyle(fill=status_color)),
                            spacing=0.3
                        ),
                        rio.Spacer(),
                        rio.Button(
                            "Ouvrir/Modifier",
                            icon="material/edit",
                            on_press=lambda id=acte.id: self.on_edit_acte(id) if self.on_edit_acte else None,
                            style="minor"
                        ),
                        spacing=2,
                        align_y=0.5
                    ),
                    margin=0.5
                )
            )
            
        return rio.Column(
            rio.Row(
                rio.Text(f"{len(actes)} acte(s)", style="heading3"),
                rio.Spacer(),
                rio.Button(
                    "Rédiger un acte",
                    icon="material/post_add",
                    on_press=self.on_new_acte if self.on_new_acte else None,
                    style="major"
                ),
                spacing=2,
                align_y=0.5
            ),
            
            rio.Spacer(height=1),
            
            rio.Column(*acte_cards, spacing=1) if acte_cards else rio.Column(
                rio.Icon("material/description", fill=rio.Color.GREY, min_width=3, min_height=3),
                rio.Text("Aucun acte rédigé", style=rio.TextStyle(fill=rio.Color.GREY)),
                align_x=0.5,
                spacing=1,
                margin_y=2
            ),
            
            spacing=1
        )
    
    def _info_row(self, label: str, value: str) -> rio.Component:
        """Helper to create an info row"""
        return rio.Row(
            rio.Text(f"{label}:", style=rio.TextStyle(font_weight="bold")),
            rio.Spacer(),
            rio.Text(value),
            spacing=1
        )

