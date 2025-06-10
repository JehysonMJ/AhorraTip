import flet as ft
from pymongo import MongoClient
import certifi
from Sesion import usuario_actual

# Conexión a MongoDB
def conectar_mongo():
    client = MongoClient("mongodb+srv://jmj252004:3lBz9QwY7Uc0If2T@ahorratip.jvgcrrh.mongodb.net/?retryWrites=true&w=majority",
                         tlsCAFile=certifi.where()
    )
    return client["AhorraTip"] #Retorna la base de datos "AhorraTip"

# Clase principal de la interfaz de inicio de sesión
class LoginApp:
    def __init__(self, page: ft.Page):
        self.page = page
        self.show_password = False  # Estado para mostrar u ocultar contraseña
        self.build()                # Construcción de la interfaz

    # Método para construir la interfaz de usuario del login
    def build(self):
         # Campo de texto para el nombre de usuario
        self.username = ft.TextField(label="Usuario", width=300)
        # Campo de texto para la contraseña con botón para mostrar/ocultar
        self.password = ft.TextField(
            label="Contraseña",
            password=True,
            width=300,
            suffix=ft.IconButton(
                icon=ft.Icons.VISIBILITY_OFF,
                on_click=self.toggle_password,
            ),
        )
        # Botones de inicio de sesión con redes sociales simulados
        social_buttons = ft.Column([
            # Google
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
            # Facebook
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
            # Instagram
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
            # Microsoft
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

        # Botón principal para iniciar sesión
        login_button = ft.ElevatedButton(
            "Iniciar Sesión",
            bgcolor="#1877F2",
            color="#FFFFFF",
            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=20)),
            width=200,
            on_click=self.login
        )

        # Botones adicionales para registrar cuenta o recuperar contraseña
        register_button = ft.TextButton("Crear Cuenta", on_click=self.register)
        forgot_button = ft.TextButton("¿Olvidaste tu contraseña?", on_click=self.recover)

        # Agrega todos los controles a la página
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

    # Método para alternar visibilidad de la contraseña
    def toggle_password(self, e):
        self.show_password = not self.show_password
        self.password.password = not self.show_password
        self.password.suffix.icon = (
            ft.Icons.VISIBILITY if self.show_password else ft.Icons.VISIBILITY_OFF
        )
        self.page.update()

    # Método para autenticar al usuario usando MongoDB
    def login(self, e): 
        from Sesion import usuario_actual   # Importa variable global del usuario

        # Obtiene la colección de usuarios
        coleccion = conectar_mongo()
        db = conectar_mongo()
        coleccion = db["usuarios"]
        usuario = self.username.value.strip()
        contrasena = self.password.value.strip()

         # Muestra una animación de carga mientras se verifica al usuario
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
             # Busca un usuario coincidente en la base de datos
            usuario_encontrado = coleccion.find_one({
                "usuario": {"$regex": f"^{usuario}$", "$options": "i"},
                "contraseña": contrasena
            })
        finally:
            # Quita la animación de carga
            self.page.overlay.remove(loading_overlay)
            self.page.update()

        if usuario_encontrado:
            # Si se encuentra el usuario, guarda su sesión y abre la app principal
            from Sesion import set_usuario_actual
            set_usuario_actual(usuario_encontrado["usuario"])
            from MainApp import MainApp
            self.page.controls.clear()
            MainApp(self.page)

        else:
            # Si no se encuentra el usuario, muestra error
            self.show_snackbar("Usuario o contraseña incorrectos.", "red")

    # Muestra pantalla de registro
    def register(self, e):
        from RegisterApp import RegisterApp
        self.page.controls.clear()
        RegisterApp(self.page)

    # Muestra pantalla de recuperación de contraseña
    def recover(self, e):
        from RecoveryApp import RecoveryApp
        self.page.controls.clear()
        RecoveryApp(self.page)

    # Simulaciones de login con redes sociales (solo impresión en consola)
    def login_google(self, e):
        print("Login con Google (simulado)")

    def login_facebook(self, e):
        print("Login con Facebook (simulado)")

    def login_instagram(self, e):
        print("Login con Instagram (simulado)")

    def login_microsoft(self, e):
        print("Login con Microsoft (simulado)")

# Función principal que inicia la app con tema oscuro y pantalla de bienvenida
def main(page: ft.Page):
    page.title = "AhorraTip APP"
    page.theme_mode = ft.ThemeMode.DARK
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    from SplashScreenApp import SplashScreenApp
    SplashScreenApp(page)

# Punto de entrada de la aplicación
if __name__ == "__main__":
    ft.app(target=main)
