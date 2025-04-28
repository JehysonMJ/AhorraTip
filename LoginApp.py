import flet as ft

class LoginApp:
    def __init__(self, page: ft.Page):
        self.page = page
        self.show_password = False
        self.build()

    def build(self):
        self.username = ft.TextField(label="Usuario", width=300)

        self.password = ft.TextField(
            label="Contraseña",
            password=True,
            width=300,
            suffix=ft.IconButton(
                icon=ft.icons.VISIBILITY_OFF,
                on_click=self.toggle_password,
            ),
        )

        # Botones sociales estilo columna
        social_buttons = ft.Column([
            ft.ElevatedButton(
                content=ft.Row([
                    ft.Image(src="https://upload.wikimedia.org/wikipedia/commons/5/53/Google_%22G%22_Logo.svg", width=20, height=20),
                    ft.Text("Google"),
                ], alignment=ft.MainAxisAlignment.CENTER, spacing=5),
                bgcolor="#FFFFFF",
                color="#000000",
                style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=20)),
                width=220,
                on_click=self.login_google,
            ),
            ft.ElevatedButton(
                content=ft.Row([
                    ft.Image(src="https://upload.wikimedia.org/wikipedia/commons/0/05/Facebook_Logo_%282019%29.png", width=20, height=20),
                    ft.Text("Facebook"),
                ], alignment=ft.MainAxisAlignment.CENTER, spacing=5),
                bgcolor="#1877F2",
                color="#FFFFFF",
                style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=20)),
                width=220,
                on_click=self.login_facebook,
            ),
            ft.ElevatedButton(
                content=ft.Row([
                    ft.Image(src="https://upload.wikimedia.org/wikipedia/commons/e/e7/Instagram_logo_2016.svg", width=20, height=20),
                    ft.Text("Instagram"),
                ], alignment=ft.MainAxisAlignment.CENTER, spacing=5),
                bgcolor="#C13584",
                color="#FFFFFF",
                style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=20)),
                width=220,
                on_click=self.login_instagram,
            ),
            ft.ElevatedButton(
                content=ft.Row([
                    ft.Image(src="https://upload.wikimedia.org/wikipedia/commons/4/44/Microsoft_logo.svg", width=20, height=20),
                    ft.Text("Microsoft"),
                ], alignment=ft.MainAxisAlignment.CENTER, spacing=5),
                bgcolor="#00A4EF",
                color="#FFFFFF",
                style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=20)),
                width=220,
                on_click=self.login_microsoft,
            ),
        ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=10)

        login_button = ft.ElevatedButton(
            "Iniciar Sesión",
            bgcolor="#1877F2",  # Verde agradable
            color="#FFFFFF",    # Texto blanco
            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=20)),
            width=200,          # Para que se vea proporcionado
            on_click=self.login
        )
        register_button = ft.TextButton("Crear Cuenta", on_click=self.register)
        forgot_button = ft.TextButton("¿Olvidaste tu contraseña?", on_click=self.recover)

        self.page.add(
            ft.Column([
                ft.Text("Bienvenido A AhorraTip", size=30, weight="bold"),
                self.username,
                self.password,
                login_button,
                ft.Row([
                    register_button,
                    forgot_button
                ], alignment=ft.MainAxisAlignment.CENTER),
                ft.Divider(),
                ft.Text("Inicia Sesión:", size=16),
                social_buttons
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=20)
        )

    def toggle_password(self, e):
        self.show_password = not self.show_password
        self.password.password = not self.show_password
        self.password.suffix.icon = (
            ft.icons.VISIBILITY if self.show_password else ft.icons.VISIBILITY_OFF
        )
        self.page.update()

    def login(self, e):
        print(f"Intentando iniciar sesión como {self.username.value}")

    def register(self, e):
        print("Ir a pantalla de Registro")

    def recover(self, e):
        print("Ir a pantalla de Recuperar Cuenta")

    def login_google(self, e):
        print("Login con Google (simulado)")

    def login_facebook(self, e):
        print("Login con Facebook (simulado)")

    def login_instagram(self, e):
        print("Login con Instagram (simulado)")

    def login_microsoft(self, e):
        print("Login con Microsoft (simulado)")


def main(page: ft.Page):
    page.title = "AhorraTip Login"
    page.theme_mode = ft.ThemeMode.DARK
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    LoginApp(page)

if __name__ == "__main__":
    ft.app(target=main)
