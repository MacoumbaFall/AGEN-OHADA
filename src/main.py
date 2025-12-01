import rio

class HomePage(rio.Component):
    def build(self) -> rio.Component:
        return rio.Column(
            rio.Text(
                "AGEN-OHADA",
                style=rio.TextStyle(font_size=2.5, font_weight="bold"),
            ),
            rio.Text(
                "Application de Gestion d'Étude Notariale OHADA",
                style=rio.TextStyle(font_size=1.2),
            ),
            rio.Spacer(height=2),
            rio.Card(
                rio.Column(
                    rio.Text("Bienvenue sur votre application de gestion notariale", style="heading3"),
                    rio.Text("Version 1.0.0 - Projet initialisé avec succès"),
                    spacing=1,
                ),
                margin=2,
            ),
            spacing=1,
            margin=2,
        )

app = rio.App(
    build=HomePage,
)

if __name__ == "__main__":
    app.run_in_browser()
