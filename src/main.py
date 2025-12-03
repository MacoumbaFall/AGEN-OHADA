import rio
from src.pages.login import LoginPage
from src.pages.dashboard import DashboardPage
from src.pages.dossiers import DossierListPage
from src.pages.dossier_form import DossierFormPage

class MainApp(rio.Component):
    """
    Main application component with session management and navigation
    """
    # Session state
    is_authenticated: bool = False
    current_user: str = ""
    current_page: str = "dashboard"
    
    def on_login_success(self, username: str):
        """Called when user successfully logs in"""
        self.is_authenticated = True
        self.current_user = username
        print(f"✅ User {username} logged in successfully")
    
    def on_logout(self):
        """Called when user logs out"""
        self.is_authenticated = False
        self.current_user = ""
        self.current_page = "dashboard"
        print("👋 User logged out")
        
    def navigate_to(self, page: str):
        self.current_page = page
    
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
                on_new_dossier=lambda: self.navigate_to("dossier_new")
            )
        elif self.current_page == "dossier_new":
            content = DossierFormPage(
                on_cancel=lambda: self.navigate_to("dossiers"),
                on_success=lambda: self.navigate_to("dossiers")
            )
        else:
            content = rio.Text("Page not found")
            
        # Layout with Sidebar and Content
        return rio.Row(
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
                        style="major" if self.current_page == "dossiers" else "colored-text",
                        on_press=lambda: self.navigate_to("dossiers")
                    ),
                    rio.Button(
                        "Actes", 
                        icon="material/description", 
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

# Create the Rio app
app = rio.App(
    build=MainApp,
    name="AGEN-OHADA"
)

if __name__ == "__main__":
    app.run_in_browser(port=8000)
