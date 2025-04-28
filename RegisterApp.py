# Importa la librería Flet para construir la interfaz gráfica.
import flet as ft

# Clase principal de la pantalla de registro de usuarios.
class RegisterApp:
    # Constructor de la clase.
    def __init__(self, page: ft.Page):
        self.page = page  # Guarda la referencia de la página.
        self.show_password = False  # Controla si la contraseña principal es visible.
        self.show_confirm_password = False  # Controla si la confirmación de contraseña es visible.
        self.build()  # Construye la interfaz.

    # Método que arma toda la interfaz gráfica de la pantalla de registro.
    def build(self):
        # Campo de texto para el nombre completo.
        self.name = ft.TextField(
            label="Nombre Completo", width=300, height=50, dense=True
        )

        # Campo de texto para el correo electrónico.
        self.email = ft.TextField(
            label="Correo Electrónico", width=300, height=50, dense=True
        )

        # Campo de texto para el nombre de usuario.
        self.username = ft.TextField(
            label="Usuario", width=300, height=50, dense=True
        )

        # Campo de texto para la contraseña.
        self.password = ft.TextField(
            label="Contraseña",
            password=True,  # Oculta el texto inicialmente.
            width=300,
            height=50,
            dense=True,
            suffix=ft.IconButton(  # Botón para alternar visibilidad.
                icon=ft.icons.VISIBILITY_OFF,
                on_click=self.toggle_password,
            ),
        )

        # Campo de texto para confirmar la contraseña.
        self.confirm_password = ft.TextField(
            label="Confirmar Contraseña",
            password=True,  # Oculta el texto inicialmente.
            width=300,
            height=50,
            dense=True,
            suffix=ft.IconButton(  # Botón para alternar visibilidad.
                icon=ft.icons.VISIBILITY_OFF,
                on_click=self.toggle_confirm_password,
            ),
        )

        # Botón para registrar una nueva cuenta.
        register_button = ft.ElevatedButton(
            "Crear Cuenta",
            bgcolor="#43D9A2",  # Color verde aguamarina para el botón.
            color="#FFFFFF",    # Texto blanco.
            style=ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(radius=20),  # Bordes redondeados.
                elevation=5,  # Sombra ligera para dar efecto flotante.
            ),
            width=220,
            height=45,
            on_click=self.register  # Acción al hacer clic: registrar usuario.
        )

        # Botón para volver al login.
        back_button = ft.TextButton(
            "Volver al Login", on_click=self.back_to_login
        )

        # Limpia cualquier contenido previo en la página.
        self.page.controls.clear()

        # Agrega todos los controles a la página organizados en una columna.
        self.page.add(
            ft.Column([
                ft.Text("Crear Cuenta", size=36, weight="bold", text_align="center"),  # Título principal.
                ft.Container(height=20),  # Espaciador.
                self.name,  # Campo Nombre.
                self.email,  # Campo Correo.
                self.username,  # Campo Usuario.
                self.password,  # Campo Contraseña.
                self.confirm_password,  # Campo Confirmar Contraseña.
                ft.Container(height=20),  # Espaciador antes del botón.
                register_button,  # Botón para crear la cuenta.
                ft.Container(height=10),  # Espaciador pequeño.
                back_button,  # Botón para volver al login.
            ],
            alignment=ft.MainAxisAlignment.CENTER,  # Centrado vertical.
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,  # Centrado horizontal.
            spacing=15)  # Espaciado entre elementos.
        )
        self.page.update()  # Actualiza la página para mostrar los cambios.

    # Método para alternar la visibilidad del campo de contraseña principal.
    def toggle_password(self, e):
        self.show_password = not self.show_password  # Cambia el estado de visibilidad.
        self.password.password = not self.show_password  # Actualiza el campo.
        self.password.suffix.icon = (
            ft.icons.VISIBILITY if self.show_password else ft.icons.VISIBILITY_OFF
        )  # Cambia el ícono del botón.
        self.page.update()  # Refresca la página.

    # Método para alternar la visibilidad del campo de confirmar contraseña.
    def toggle_confirm_password(self, e):
        self.show_confirm_password = not self.show_confirm_password  # Cambia el estado de visibilidad.
        self.confirm_password.password = not self.show_confirm_password  # Actualiza el campo.
        self.confirm_password.suffix.icon = (
            ft.icons.VISIBILITY if self.show_confirm_password else ft.icons.VISIBILITY_OFF
        )  # Cambia el ícono del botón.
        self.page.update()  # Refresca la página.

    # Método que procesa el registro del usuario.
    def register(self, e):
        # Verifica que todos los campos estén llenos.
        if not all([
            self.name.value,
            self.email.value,
            self.username.value,
            self.password.value,
            self.confirm_password.value
        ]):
            # Muestra un mensaje de error si falta algún campo.
            self.page.snack_bar = ft.SnackBar(ft.Text("Completa todos los campos."), bgcolor="red")
            self.page.snack_bar.open = True
            self.page.update()
            return

        # Verifica que las contraseñas coincidan.
        if self.password.value != self.confirm_password.value:
            # Muestra un mensaje de error si las contraseñas no coinciden.
            self.page.snack_bar = ft.SnackBar(ft.Text("Las contraseñas no coinciden."), bgcolor="red")
            self.page.snack_bar.open = True
            self.page.update()
            return

        # Si todo es correcto, muestra mensaje de éxito.
        self.page.snack_bar = ft.SnackBar(ft.Text("¡Cuenta creada exitosamente! 🎉"), bgcolor="green")
        self.page.snack_bar.open = True
        self.page.update()

    # Método que regresa a la pantalla de login.
    def back_to_login(self, e):
        from LoginApp import LoginApp  # Importa dinámicamente la pantalla de login.
        self.page.controls.clear()  # Limpia la página.
        LoginApp(self.page)  # Carga la clase LoginApp.
