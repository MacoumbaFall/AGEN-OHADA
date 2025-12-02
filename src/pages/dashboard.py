import rio

class DashboardPage(rio.Component):
    def build(self) -> rio.Component:
        return rio.Column(
            rio.Text("Tableau de Bord", style="heading1"),
            rio.Row(
                rio.Card(
                    rio.Column(
                        rio.Text("Dossiers en cours", style="heading3"),
                        rio.Text("12", style=rio.TextStyle(font_size=3, font_weight="bold")),
                        spacing=1
                    ),
                    margin=1,
                    grow=1
                ),
                rio.Card(
                    rio.Column(
                        rio.Text("Actes à signer", style="heading3"),
                        rio.Text("3", style=rio.TextStyle(font_size=3, font_weight="bold", fill=rio.Color.ORANGE)),
                        spacing=1
                    ),
                    margin=1,
                    grow=1
                ),
                rio.Card(
                    rio.Column(
                        rio.Text("Formalités", style="heading3"),
                        rio.Text("5", style=rio.TextStyle(font_size=3, font_weight="bold", fill=rio.Color.BLUE)),
                        spacing=1
                    ),
                    margin=1,
                    grow=1
                ),
                spacing=2
            ),
            rio.Spacer(height=2),
            rio.Text("Bienvenue sur AGEN-OHADA", style="text-dim"),
            spacing=2,
            margin=2
        )
