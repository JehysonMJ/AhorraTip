# Importa la librería Flet para crear la interfaz gráfica.
import flet as ft

# Clase principal de la aplicación de login.
class LoginApp:
    # Constructor de la clase.
    def __init__(self, page: ft.Page):
        self.page = page  # Guarda la referencia a la página de Flet.
        self.show_password = False  # Variable para controlar si se muestra o no la contraseña.
        self.build()  # Llama al método que construye la interfaz.

    # Método que construye la interfaz de usuario.
    def build(self):
        # Campo de texto para el nombre de usuario.
        self.username = ft.TextField(label="Usuario", width=300)

        # Campo de texto para la contraseña con opción de mostrar/ocultar.
        self.password = ft.TextField(
            label="Contraseña",
            password=True,  # Inicialmente el texto estará oculto (tipo password).
            width=300,
            suffix=ft.IconButton(  # Botón al final del campo para mostrar/ocultar contraseña.
                icon=ft.icons.VISIBILITY_OFF,  # Ícono inicial (ojo cerrado).
                on_click=self.toggle_password,  # Al hacer clic se alterna la visibilidad.
            ),
        )

        # Botones sociales agrupados en una columna.
        social_buttons = ft.Column([
            # Botón de inicio de sesión con Google.
            ft.ElevatedButton(
                content=ft.Row([
                    ft.Image(src="https://upload.wikimedia.org/wikipedia/commons/5/53/Google_%22G%22_Logo.svg", width=20, height=20),  # Logo de Google.
                    ft.Text("Google"),  # Texto "Google".
                ], alignment=ft.MainAxisAlignment.CENTER, spacing=5),
                bgcolor="#FFFFFF",  # Fondo blanco.
                color="#000000",    # Texto negro.
                style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=20)),  # Bordes redondeados.
                width=220,
                on_click=self.login_google,  # Acción simulada de login con Google.
            ),
            # Botón de inicio de sesión con Facebook.
            ft.ElevatedButton(
                content=ft.Row([
                    ft.Image(src="https://upload.wikimedia.org/wikipedia/commons/0/05/Facebook_Logo_%282019%29.png", width=20, height=20),  # Logo de Facebook.
                    ft.Text("Facebook"),  # Texto "Facebook".
                ], alignment=ft.MainAxisAlignment.CENTER, spacing=5),
                bgcolor="#1877F2",  # Fondo azul Facebook.
                color="#FFFFFF",    # Texto blanco.
                style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=20)),
                width=220,
                on_click=self.login_facebook,  # Acción simulada de login con Facebook.
            ),
            # Botón de inicio de sesión con Instagram.
            ft.ElevatedButton(
                content=ft.Row([
                    ft.Image(src="https://upload.wikimedia.org/wikipedia/commons/e/e7/Instagram_logo_2016.svg", width=20, height=20),  # Logo de Instagram.
                    ft.Text("Instagram"),  # Texto "Instagram".
                ], alignment=ft.MainAxisAlignment.CENTER, spacing=5),
                bgcolor="#C13584",  # Fondo rosado Instagram.
                color="#FFFFFF",
                style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=20)),
                width=220,
                on_click=self.login_instagram,  # Acción simulada de login con Instagram.
            ),
            # Botón de inicio de sesión con Microsoft.
            ft.ElevatedButton(
                content=ft.Row([
                    ft.Image(src="https://upload.wikimedia.org/wikipedia/commons/4/44/Microsoft_logo.svg", width=20, height=20),  # Logo de Microsoft.
                    ft.Text("Microsoft"),  # Texto "Microsoft".
                ], alignment=ft.MainAxisAlignment.CENTER, spacing=5),
                bgcolor="#00A4EF",  # Fondo azul Microsoft.
                color="#FFFFFF",
                style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=20)),
                width=220,
                on_click=self.login_microsoft,  # Acción simulada de login con Microsoft.
            ),
        ],
        alignment=ft.MainAxisAlignment.CENTER,  # Alinea verticalmente al centro.
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,  # Alinea horizontalmente al centro.
        spacing=10)  # Espaciado de 10 entre botones.

        # Botón principal de iniciar sesión.
        login_button = ft.ElevatedButton(
            "Iniciar Sesión",
            bgcolor="#1877F2",  # Fondo azul.
            color="#FFFFFF",    # Texto blanco.
            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=20)),  # Bordes redondeados.
            width=200,
            on_click=self.login  # Acción de login (simulada).
        )

        # Botón de crear cuenta (registro).
        register_button = ft.TextButton(
            "Crear Cuenta", on_click=self.register
        )

        # Botón de recuperar contraseña.
        forgot_button = ft.TextButton(
            "¿Olvidaste tu contraseña?", on_click=self.recover
        )

        # Agrega todos los elementos a la página.
        self.page.add(
            ft.Column([
                ft.Text("Bienvenido A AhorraTip", size=30, weight="bold"),  # Título principal.
                self.username,  # Campo de usuario.
                self.password,  # Campo de contraseña.
                login_button,  # Botón de iniciar sesión.
                ft.Row([  # Fila que contiene "Crear Cuenta" y "¿Olvidaste tu contraseña?".
                    register_button,
                    forgot_button
                ], alignment=ft.MainAxisAlignment.CENTER),
                ft.Divider(),  # Línea divisoria.
                ft.Text("Inicia Sesión:", size=16),  # Subtítulo para los botones sociales.
                social_buttons  # Botones sociales.
            ],
            alignment=ft.MainAxisAlignment.CENTER,  # Centrado vertical.
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,  # Centrado horizontal.
            spacing=20)  # Espaciado entre componentes.
        )

    # Método para alternar la visibilidad de la contraseña.
    def toggle_password(self, e):
        self.show_password = not self.show_password  # Cambia el estado de visibilidad.
        self.password.password = not self.show_password  # Actualiza el campo para mostrar/ocultar el texto.
        self.password.suffix.icon = (  # Cambia el ícono según el estado.
            ft.icons.VISIBILITY if self.show_password else ft.icons.VISIBILITY_OFF
        )
        self.page.update()  # Actualiza la página para reflejar los cambios.

    # Acción al presionar el botón "Iniciar Sesión".
    def login(self, e):
        print(f"Intentando iniciar sesión como {self.username.value}")  # Imprime el usuario ingresado.

    # Acción al presionar "Crear Cuenta".
    def register(self, e):
        from RegisterApp import RegisterApp
        self.page.controls.clear()
        RegisterApp(self.page)

    # Acción al presionar "¿Olvidaste tu contraseña?".
    def recover(self, e):
        print("Ir a pantalla de Recuperar Cuenta")  # Simula ir a la pantalla de recuperación.

    # Acción simulada de login con Google.
    def login_google(self, e):
        print("Login con Google (simulado)")

    # Acción simulada de login con Facebook.
    def login_facebook(self, e):
        print("Login con Facebook (simulado)")

    # Acción simulada de login con Instagram.
    def login_instagram(self, e):
        print("Login con Instagram (simulado)")

    # Acción simulada de login con Microsoft.
    def login_microsoft(self, e):
        print("Login con Microsoft (simulado)")

# Función principal que configura la página principal.
def main(page: ft.Page):
    page.title = "AhorraTip Login"  # Título de la ventana.
    page.theme_mode = ft.ThemeMode.DARK  # Tema oscuro activado.
    page.vertical_alignment = ft.MainAxisAlignment.CENTER  # Centrado vertical de los elementos.
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER  # Centrado horizontal de los elementos.
    LoginApp(page)  # Crea una instancia de la aplicación de login.

# Verifica que se esté ejecutando este archivo como programa principal.
if __name__ == "__main__":
    ft.app(target=main)  # Ejecuta la app en Flet apuntando a la función principal.
