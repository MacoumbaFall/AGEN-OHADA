import rio
from src.pages.login import LoginPage
from src.pages.dashboard import DashboardPage

class MainApp(rio.Component):
    """
    Main application component with session management
    """
    # Session state
    is_authenticated: bool = False
    current_user: str = ""
    
    def on_login_success(self, username: str):
        """Called when user successfully logs in"""
        self.is_authenticated = True
        self.current_user = username
        print(f"✅ User {username} logged in successfully")
    
    def on_logout(self):
        """Called when user logs out"""
        self.is_authenticated = False
        self.current_user = ""
        print("👋 User logged out")
    
    def build(self) -> rio.Component:
        # Show login page if not authenticated
        if not self.is_authenticated:
            return rio.Column(
                LoginPage(
                    on_success=lambda: self.on_login_success("admin")
                ),
                align_x=0.5,
                align_y=0.5,
            )
        
        # Show dashboard with navigation if authenticated
        return rio.Column(
            # Header
            rio.Card(
                rio.Row(
                    rio.Text(
                        "AGEN-OHADA",
                        style=rio.TextStyle(
                            font_size=1.5,
                            font_weight="bold"
                        )
                    ),
                    rio.Spacer(),
                    rio.Text(
                        f"👤 {self.current_user}",
                        style="text-dim"
                    ),
                    rio.Button(
                        "Déconnexion",
                        on_press=self.on_logout,
                        style="minor"
                    ),
                    spacing=2,
                    margin=1,
                ),
                color=rio.Color.from_hex("1e293b"),
            ),
            # Main content
            DashboardPage(),
            spacing=0,
        )

# Create the Rio app
app = rio.App(
    build=MainApp,
    name="AGEN-OHADA"
)

if __name__ == "__main__":
    app.run_in_browser(port=8000)
