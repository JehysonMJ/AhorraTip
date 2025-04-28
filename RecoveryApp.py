# Importaciones necesarias
import flet as ft  # Librería Flet para crear la interfaz gráfica
import re  # Librería re para validación de correos electrónicos
import time  # Librería time para simular una espera (loader)

# Clase principal para la recuperación de contraseña
class RecoveryApp:
    # Constructor de la clase
    def __init__(self, page: ft.Page):
        self.page = page  # Guarda la referencia de la página
        self.build()  # Construye la interfaz gráfica

    # Método que construye la pantalla de recuperación
    def build(self):
        # Campo de entrada para el correo electrónico
        self.email = ft.TextField(
            label="Correo Electrónico",  # Etiqueta del campo
            width=300,
            height=50,
            dense=True,  # Diseño compacto
        )

        # Botón para enviar solicitud de recuperación
        recover_button = ft.ElevatedButton(
            "Recuperar Contraseña",  # Texto del botón
            bgcolor="#5C9EFF",  # Color de fondo azul
            color="#FFFFFF",  # Texto blanco
            style=ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(radius=20),  # Bordes redondeados
                elevation=5,  # Sombra de elevación
            ),
            width=220,
            height=45,
            on_click=self.recover_password  # Llama al método para recuperar la contraseña
        )

        # Botón para volver a la pantalla de login
        back_button = ft.TextButton(
            "Volver al Login", on_click=self.back_to_login
        )

        # Limpiamos los controles actuales y agregamos nuevos elementos
        self.page.controls.clear()
        self.page.add(
            ft.Column([
                ft.Text("Recuperar Contraseña", size=36, weight="bold", text_align="center"),  # Título de la pantalla
                ft.Container(height=10),  # Espaciador
                ft.Image(
                    src="assets/Contrseña.png",  # Imagen ilustrativa
                    width=200,
                    height=200,
                    fit=ft.ImageFit.CONTAIN  # Ajuste proporcional de la imagen
                ),
                ft.Container(height=20),  # Espaciador
                self.email,  # Campo de email
                ft.Container(height=20),  # Espaciador
                recover_button,  # Botón de recuperación
                ft.Container(height=10),  # Espaciador
                back_button,  # Botón para regresar
            ],
            alignment=ft.MainAxisAlignment.CENTER,  # Alineación vertical al centro
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,  # Alineación horizontal al centro
            spacing=15)  # Espaciado entre los elementos
        )
        self.page.update()  # Actualiza la pantalla para mostrar los cambios

    # Método que procesa la recuperación de contraseña
    def recover_password(self, e):
        # Validar que el campo de correo no esté vacío
        if not self.email.value:
            self.show_snackbar("Por favor ingresa tu correo electrónico.", "red")
            return

        # Validar formato de correo electrónico usando expresión regular
        if not re.match(r"[^@]+@[^@]+\.[^@]+", self.email.value):
            self.show_snackbar("Correo electrónico no válido.", "red")
            return

        # Muestra un loader simulando el envío del correo
        self.page.overlay.append(
            ft.ProgressBar(width=300)  # Barra de progreso visible
        )
        self.page.update()

        time.sleep(2)  # Simula un tiempo de espera de 2 segundos

        # Quitar el loader una vez terminado el proceso
        self.page.overlay.clear()

        # Simulación: si el correo contiene "noexiste", simulamos que no está registrado
        if "noexiste" in self.email.value.lower():
            self.show_dialog(
                "Correo no encontrado",  # Título del cuadro de diálogo
                "El correo ingresado no está registrado. Intenta nuevamente.",  # Mensaje
                success=False  # Estilo de error
            )
        else:
            self.show_dialog(
                "Correo Enviado",  # Título del cuadro de diálogo
                "¡Te hemos enviado instrucciones a tu correo! 📧",  # Mensaje
                success=True  # Estilo de éxito
            )

    # Método para mostrar un mensaje tipo snackbar en la parte inferior
    def show_snackbar(self, message, color):
        self.page.snack_bar = ft.SnackBar(
            content=ft.Text(message),  # Contenido del mensaje
            bgcolor=color  # Color de fondo (rojo o verde)
        )
        self.page.snack_bar.open = True  # Abre el snackbar
        self.page.update()

    # Método para mostrar un cuadro de diálogo personalizado
    def show_dialog(self, title, message, success=True):
        self.dialog = ft.AlertDialog(
            modal=True,  # El usuario debe interactuar con el diálogo para cerrarlo
            title=ft.Text(title, weight="bold", size=24),  # Título del diálogo
            content=ft.Text(message, size=16),  # Contenido del diálogo
            actions=[
                ft.TextButton(
                    "OK",
                    on_click=self.close_dialog,  # Cierra el cuadro de diálogo al hacer clic
                    style=ft.ButtonStyle(
                        bgcolor="#43D9A2" if success else "#FF5C5C",  # Verde si es éxito, rojo si es error
                        color="white",  # Color del texto
                        shape=ft.RoundedRectangleBorder(radius=15)  # Bordes redondeados
                    )
                )
            ],
        )
        self.page.dialog = self.dialog  # Asigna el cuadro de diálogo a la página
        self.dialog.open = True  # Abre el cuadro de diálogo
        self.page.update()

    # Método para cerrar el cuadro de diálogo
    def close_dialog(self, e):
        self.dialog.open = False  # Cierra el diálogo
        self.page.update()

    # Método para regresar a la pantalla de login
    def back_to_login(self, e):
        from LoginApp import LoginApp  # Importa la clase LoginApp
        self.page.controls.clear()  # Limpia la pantalla actual
        LoginApp(self.page)  # Carga la pantalla de Login
