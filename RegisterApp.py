# Importamos las librerías necesarias
import flet as ft  # Flet para crear la interfaz gráfica
import re  # re para validaciones de texto como correos electrónicos
import time  # time para simular carga (pausas)

# Clase principal que representa la pantalla de registro de usuarios
class RegisterApp:
    def __init__(self, page: ft.Page):
        self.page = page  # Guarda la referencia de la página
        self.show_password = False  # Controla visibilidad de la contraseña
        self.show_confirm_password = False  # Controla visibilidad de confirmar contraseña
        self.build()  # Llama a construir la interfaz

    # Método que construye todos los componentes de la pantalla
    def build(self):
        # Campos de entrada
        self.name = ft.TextField(label="Nombre Completo", width=300, height=50, dense=True)
        self.email = ft.TextField(label="Correo Electrónico", width=300, height=50, dense=True)
        self.username = ft.TextField(label="Usuario", width=300, height=50, dense=True)
        
        # Campo para contraseña con botón para mostrar/ocultar
        self.password = ft.TextField(
            label="Contraseña",
            password=True,
            width=300,
            height=50,
            dense=True,
            suffix=ft.IconButton(
                icon=ft.icons.VISIBILITY_OFF,  # Icono de ojo cerrado
                on_click=self.toggle_password,  # Al hacer clic cambia visibilidad
            ),
        )
        
        # Campo para confirmar la contraseña con botón para mostrar/ocultar
        self.confirm_password = ft.TextField(
            label="Confirmar Contraseña",
            password=True,
            width=300,
            height=50,
            dense=True,
            suffix=ft.IconButton(
                icon=ft.icons.VISIBILITY_OFF,
                on_click=self.toggle_confirm_password,
            ),
        )

        # Botón de "Crear Cuenta"
        register_button = ft.ElevatedButton(
            "Crear Cuenta",
            bgcolor="#43D9A2",  # Color verde agua
            color="#FFFFFF",  # Texto blanco
            style=ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(radius=20),  # Botón redondeado
                elevation=5,  # Sombra ligera
            ),
            width=220,
            height=45,
            on_click=self.confirm_register  # Llama a confirmación antes de registrar
        )

        # Botón para regresar al login
        back_button = ft.TextButton("Volver al Login", on_click=self.back_to_login)

        # Limpia controles previos y agrega los nuevos en un contenedor organizado
        self.page.controls.clear()
        self.page.add(
            ft.Column([
                ft.Text("Crear Cuenta", size=36, weight="bold", text_align="center"),  # Título
                ft.Container(height=20),  # Espaciador
                self.name,
                self.email,
                self.username,
                self.password,
                self.confirm_password,
                ft.Container(height=20),  # Espaciador
                register_button,
                ft.Container(height=10),
                back_button,
            ],
            alignment=ft.MainAxisAlignment.CENTER,  # Centrado vertical
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,  # Centrado horizontal
            spacing=15)  # Espacio entre elementos
        )
        self.page.update()  # Actualiza la página

    # Método para alternar visibilidad de la contraseña principal
    def toggle_password(self, e):
        self.show_password = not self.show_password  # Cambia el estado
        self.password.password = not self.show_password  # Actualiza campo
        self.password.suffix.icon = (
            ft.icons.VISIBILITY if self.show_password else ft.icons.VISIBILITY_OFF
        )  # Cambia el icono
        self.page.update()

    # Método para alternar visibilidad de confirmar contraseña
    def toggle_confirm_password(self, e):
        self.show_confirm_password = not self.show_confirm_password
        self.confirm_password.password = not self.show_confirm_password
        self.confirm_password.suffix.icon = (
            ft.icons.VISIBILITY if self.show_confirm_password else ft.icons.VISIBILITY_OFF
        )
        self.page.update()

    # Método que lanza un cuadro de confirmación antes de registrar
    def confirm_register(self, e):
        self.dialog = ft.AlertDialog(
            modal=True,  # No permite interactuar fuera del cuadro
            title=ft.Text("Confirmar Registro"),  # Título del cuadro
            content=ft.Text("¿Seguro que quieres crear la cuenta?"),  # Mensaje
            actions=[  # Botones del cuadro
                ft.TextButton("Cancelar", on_click=self.close_dialog),
                ft.TextButton("Sí, crear cuenta", on_click=self.register),
            ],
        )
        self.page.dialog = self.dialog
        self.dialog.open = True  # Abre el cuadro
        self.page.update()

    # Cierra el cuadro de diálogo
    def close_dialog(self, e):
        self.dialog.open = False
        self.page.update()

    # Método principal para procesar el registro
    def register(self, e):
        self.dialog.open = False  # Cierra el cuadro de confirmación
        self.page.update()

        # Validar que todos los campos estén llenos
        if not all([self.name.value, self.email.value, self.username.value, self.password.value, self.confirm_password.value]):
            self.show_snackbar("Completa todos los campos.", "red")
            return

        # Validar el formato del correo electrónico
        if not self.is_valid_email(self.email.value):
            self.show_snackbar("Correo electrónico no válido.", "red")
            return

        # Validar que las contraseñas coincidan
        if self.password.value != self.confirm_password.value:
            self.show_snackbar("Las contraseñas no coinciden.", "red")
            return

        # Simular proceso de creación de cuenta
        self.page.overlay.append(
            ft.ProgressBar(width=300)  # Muestra barra de carga
        )
        self.page.update()
        time.sleep(2)  # Simula una espera de 2 segundos (carga)

        # Quitar el loader
        self.page.overlay.clear()
        # Mostrar mensaje de éxito
        self.show_snackbar("¡Cuenta creada exitosamente! 🎉", "green")

    # Función auxiliar para mostrar snackbars (mensajes emergentes abajo)
    def show_snackbar(self, message, color):
        self.page.snack_bar = ft.SnackBar(
            content=ft.Text(message),  # Mensaje
            bgcolor=color  # Color de fondo
        )
        self.page.snack_bar.open = True  # Abre el snackbar
        self.page.update()

    # Función para validar el formato de un correo electrónico
    def is_valid_email(self, email):
        return bool(re.match(r"[^@]+@[^@]+\.[^@]+", email))  # Patrón simple de validación

    # Método para regresar a la pantalla de login
    def back_to_login(self, e):
        from LoginApp import LoginApp  # Importa la clase LoginApp
        self.page.controls.clear()  # Limpia controles actuales
        LoginApp(self.page)  # Carga la pantalla de login
