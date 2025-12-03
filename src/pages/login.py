import rio
from src.database import get_db
from src.models.user import User
from src.auth import verify_password

class LoginPage(rio.Component):
    username: str = ""
    password: str = ""
    error_message: str = ""
    
    # Callback function to call on successful login
    # This will be passed by the parent component
    on_success: rio.EventHandler[str] = None

    def on_login(self):
        db = next(get_db())
        user = db.query(User).filter(User.username == self.username).first()
        
        if not user or not verify_password(self.password, user.password_hash):
            self.error_message = "Nom d'utilisateur ou mot de passe incorrect"
            return

        print(f"Login successful for {user.username}")
        
        # Clear error message
        self.error_message = ""
        
        # Trigger the success event with username
        if self.on_success:
            self.on_success(user.username)

    def build(self) -> rio.Component:
        return rio.Column(
            rio.Text("AGEN-OHADA", style=rio.TextStyle(font_size=2, font_weight="bold")),
            rio.Text("Connexion", style="heading2"),
            rio.TextInput(
                label="Nom d'utilisateur",
                text=self.bind().username,
            ),
            rio.TextInput(
                label="Mot de passe",
                text=self.bind().password,
                is_secret=True,
            ),
            rio.Button("Se connecter", on_press=self.on_login),
            rio.Text(self.error_message, style=rio.TextStyle(fill=rio.Color.RED)) if self.error_message else rio.Text(""),
            spacing=1,
            margin=2,
            align_x=0.5,
            align_y=0.5,
        )
