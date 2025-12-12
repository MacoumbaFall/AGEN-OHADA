from __future__ import annotations
import rio
from src.pages.login import LoginPage
from src.pages.dashboard import DashboardPage
from src.pages.dossiers import DossierListPage
from src.pages.dossier_form import DossierFormPage
from src.pages.dossier_detail import DossierDetailPage
from src.pages.dossier_edit import DossierEditPage
from src.pages.templates import TemplatesPage
from src.pages.acte_edit import ActeEditPage
from src.database import get_db
from src.models.dossier import Dossier

class MainApp(rio.Component):
    """
    Main application component with session management and navigation
    """
    # Session state
    is_authenticated: bool = False
    current_user: str = ""
    current_page: str = "dashboard"
    current_dossier_id: int = None
    current_acte_id: int = None

    
    # Delete confirmation state
    show_delete_dialog: bool = False
    dossier_to_delete_id: int = None
    
    def on_login_success(self, username: str):
        """Called when user successfully logs in"""
        self.is_authenticated = True
        self.current_user = username
        print(f"[INFO] User {username} logged in successfully")
    
    def on_logout(self):
        """Called when user logs out"""
        self.is_authenticated = False
        self.current_user = ""
        self.current_page = "dashboard"
        print("[INFO] User logged out")
        
    def navigate_to(self, page: str, dossier_id: int = None, acte_id: int = None):
        """Navigate to a specific page"""
        self.current_page = page
        if dossier_id is not None:
             self.current_dossier_id = dossier_id
        if acte_id is not None:
             self.current_acte_id = acte_id
        elif page == "acte_new":
             self.current_acte_id = None

    
    def on_delete_request(self, dossier_id: int):
        """Show delete confirmation dialog"""
        self.dossier_to_delete_id = dossier_id
        self.show_delete_dialog = True
    
    def on_delete_confirm(self):
        """Confirm and execute deletion"""
        try:
            db = next(get_db())
            dossier = db.query(Dossier).filter(Dossier.id == self.dossier_to_delete_id).first()
            
            if dossier:
                # Soft delete: change status to ARCHIVE
                dossier.statut = "ARCHIVE"
                db.commit()
                print(f"✅ Dossier {dossier.numero_dossier} archived successfully")
                
                # Navigate back to list
                self.navigate_to("dossiers")
            
        except Exception as e:
            print(f"❌ Error deleting dossier: {str(e)}")
            db.rollback()
        finally:
            self.show_delete_dialog = False
            self.dossier_to_delete_id = None
    
    def on_delete_cancel(self):
        """Cancel deletion"""
        self.show_delete_dialog = False
        self.dossier_to_delete_id = None
    
    def build(self) -> rio.Component:
        # Show login page if not authenticated
        if not self.is_authenticated:
            return rio.Column(
                LoginPage(
                    on_success=self.on_login_success
                ),
                align_x=0.5,
                align_y=0.5,
            )
        
        # Determine content based on current page
        if self.current_page == "dashboard":
            content = DashboardPage()
        elif self.current_page == "dossiers":
            content = DossierListPage(
                on_new_dossier=lambda: self.navigate_to("dossier_new"),
                on_view_dossier=lambda dossier_id: self.navigate_to("dossier_detail", dossier_id)
            )
        elif self.current_page == "dossier_new":
            content = DossierFormPage(
                on_cancel=lambda: self.navigate_to("dossiers"),
                on_success=lambda: self.navigate_to("dossiers")
            )
        elif self.current_page == "dossier_detail":
            content = DossierDetailPage(
                dossier_id=self.current_dossier_id,
                on_back=lambda: self.navigate_to("dossiers"),
                on_edit=lambda dossier_id: self.navigate_to("dossier_edit", dossier_id),
                on_delete=self.on_delete_request,
                on_new_acte=lambda: self.navigate_to("acte_new", dossier_id=self.current_dossier_id),
                on_edit_acte=lambda acte_id: self.navigate_to("acte_edit", dossier_id=self.current_dossier_id, acte_id=acte_id)
            )
        elif self.current_page == "dossier_edit":
            content = DossierEditPage(
                dossier_id=self.current_dossier_id,
                current_username=self.current_user,
                on_cancel=lambda: self.navigate_to("dossier_detail", self.current_dossier_id),
                on_success=lambda dossier_id: self.navigate_to("dossier_detail", dossier_id)
            )
        elif self.current_page == "acte_new":
            content = ActeEditPage(
                dossier_id=self.current_dossier_id,
                on_cancel=lambda: self.navigate_to("dossier_detail", self.current_dossier_id),
                on_success=lambda: self.navigate_to("dossier_detail", self.current_dossier_id)
            )
        elif self.current_page == "acte_edit":
            content = ActeEditPage(
                dossier_id=self.current_dossier_id,
                acte_id=self.current_acte_id,
                on_cancel=lambda: self.navigate_to("dossier_detail", self.current_dossier_id),
                on_success=lambda: self.navigate_to("dossier_detail", self.current_dossier_id)
            )
        elif self.current_page == "templates":
            content = TemplatesPage()
        else:
            content = rio.Text("Page not found")
        
        # Main layout
        main_layout = rio.Row(
            # Sidebar
            rio.Card(
                rio.Column(
                    rio.Text("AGEN-OHADA", style=rio.TextStyle(font_size=1.5, font_weight="bold", fill=rio.Color.WHITE)),
                    rio.Spacer(height=2),
                    
                    # Navigation Menu
                    rio.Button(
                        "Tableau de Bord", 
                        icon="material/dashboard", 
                        style="major" if self.current_page == "dashboard" else "colored-text",
                        on_press=lambda: self.navigate_to("dashboard")
                    ),
                    rio.Button(
                        "Dossiers", 
                        icon="material/folder", 
                        style="major" if self.current_page.startswith("dossier") else "colored-text",
                        on_press=lambda: self.navigate_to("dossiers")
                    ),
                    rio.Button(
                        "Modèles", 
                        icon="material/description", 
                        style="major" if self.current_page == "templates" else "colored-text",
                        on_press=lambda: self.navigate_to("templates")
                    ),
                    rio.Button(
                        "Actes", 
                        icon="material/gavel", 
                        style="colored-text",
                        on_press=lambda: print("Actes: Not implemented yet")
                    ),
                    rio.Button(
                        "Clients", 
                        icon="material/groups", 
                        style="colored-text",
                        on_press=lambda: print("Clients: Not implemented yet")
                    ),
                    rio.Button(
                        "Comptabilité", 
                        icon="material/account_balance", 
                        style="colored-text",
                        on_press=lambda: print("Compta: Not implemented yet")
                    ),
                    
                    rio.Spacer(),
                    
                    # User Info & Logout
                    rio.Row(
                        rio.Icon("material/person", fill=rio.Color.WHITE),
                        rio.Text(self.current_user, style=rio.TextStyle(fill=rio.Color.WHITE)),
                        spacing=1
                    ),
                    rio.Button(
                        "Déconnexion",
                        icon="material/logout",
                        on_press=self.on_logout,
                        style="colored-text"
                    ),
                    spacing=1,
                    margin=1
                ),
                color=rio.Color.from_hex("1e293b"),
                min_width=18,
                grow_y=True
            ),
            
            # Main Content Area
            rio.Column(
                content,
                grow_x=True,
                grow_y=True,
                margin=2
            ),
            grow_x=True,
            grow_y=True
        )
        
        # Overlay delete confirmation dialog if needed
        if self.show_delete_dialog:
            return rio.Overlay(
                main_layout,
                rio.Card(
                    rio.Column(
                        rio.Icon("material/warning", fill=rio.Color.from_hex("f59e0b"), min_width=4, min_height=4),
                        rio.Text("Confirmer la suppression", style="heading2"),
                        rio.Text(
                            "Êtes-vous sûr de vouloir archiver ce dossier ? Cette action peut être annulée en changeant le statut.",
                            style="text-dim"
                        ),
                        rio.Spacer(height=2),
                        rio.Row(
                            rio.Button(
                                "Annuler",
                                on_press=self.on_delete_cancel,
                                style="minor"
                            ),
                            rio.Spacer(),
                            rio.Button(
                                "Confirmer la suppression",
                                icon="material/delete",
                                on_press=self.on_delete_confirm,
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
        
        return main_layout

# Create the Rio app
app = rio.App(
    build=MainApp,
    name="AGEN-OHADA"
)

if __name__ == "__main__":
    # Use run_as_web_server to allow IDE integrated browser
    # Access at: http://localhost:8000
    app.run_as_web_server(
        host="localhost",
        port=8000,
        quiet=False
    )
