import flet as ft
from pymongo import MongoClient
import certifi
from Sesion import usuario_actual

# Conexión a MongoDB
def conectar_mongo():
    client = MongoClient("mongodb+srv://jmj252004:3lBz9QwY7Uc0If2T@ahorratip.jvgcrrh.mongodb.net/?retryWrites=true&w=majority",
                         tlsCAFile=certifi.where()
    )
    return client["AhorraTip"]

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
                icon=ft.Icons.VISIBILITY_OFF,
                on_click=self.toggle_password,
            ),
        )

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
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=10)

        login_button = ft.ElevatedButton(
            "Iniciar Sesión",
            bgcolor="#1877F2",
            color="#FFFFFF",
            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=20)),
            width=200,
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
                ft.Row([register_button, forgot_button], alignment=ft.MainAxisAlignment.CENTER),
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
            ft.Icons.VISIBILITY if self.show_password else ft.Icons.VISIBILITY_OFF
        )
        self.page.update()

    # ✅ LOGIN CONECTADO A MONGO DB
    def login(self, e): 
        from Sesion import usuario_actual  # Importa nuestra variable global

        coleccion = conectar_mongo()
        db = conectar_mongo()
        coleccion = db["usuarios"]
        usuario = self.username.value.strip()
        contrasena = self.password.value.strip()

        # Indicador de carga con imagen GIF personalizada
        loading_overlay = ft.Container(
            content=ft.Column([
                ft.Image(src="assets/loading.gif", width=80, height=80),
                ft.Text("Verificando...", size=14, color="white")
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            alignment=ft.alignment.center,
            bgcolor=ft.Colors.with_opacity(0.6, ft.Colors.BLACK),
            width=self.page.width,
            height=self.page.height
        )

        self.page.overlay.append(loading_overlay)
        self.page.update()

        try:
            usuario_encontrado = coleccion.find_one({
                "usuario": {"$regex": f"^{usuario}$", "$options": "i"},
                "contraseña": contrasena
            })
        finally:
            self.page.overlay.remove(loading_overlay)
            self.page.update()

        if usuario_encontrado:
            from Sesion import set_usuario_actual
            set_usuario_actual(usuario_encontrado["usuario"])  # ✅ ASIGNA EL NOMBRE AL USUARIO
            from MainApp import MainApp
            self.page.controls.clear()
            MainApp(self.page)

        else:
            self.show_snackbar("Usuario o contraseña incorrectos.", "red")

    def register(self, e):
        from RegisterApp import RegisterApp
        self.page.controls.clear()
        RegisterApp(self.page)

    def recover(self, e):
        from RecoveryApp import RecoveryApp
        self.page.controls.clear()
        RecoveryApp(self.page)

    def login_google(self, e):
        print("Login con Google (simulado)")

    def login_facebook(self, e):
        print("Login con Facebook (simulado)")

    def login_instagram(self, e):
        print("Login con Instagram (simulado)")

    def login_microsoft(self, e):
        print("Login con Microsoft (simulado)")

def main(page: ft.Page):
    page.title = "AhorraTip APP"
    page.theme_mode = ft.ThemeMode.DARK
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    from SplashScreenApp import SplashScreenApp
    SplashScreenApp(page)

if __name__ == "__main__":
    ft.app(target=main)
