# Importaciones necesarias
import flet as ft  # Librería Flet para crear la interfaz gráfica
import re  # Librería re para validación de correos electrónicos
import time  # Librería time para simular una carga o proceso de espera
from pymongo import MongoClient
import certifi

def conectar_mongo():
    client = MongoClient("mongodb+srv://jmj252004:3lBz9QwY7Uc0If2T@ahorratip.jvgcrrh.mongodb.net/", tlsCAFile=certifi.where())
    db = client["AhorraTip"]
    return db["usuarios"]


# Clase principal para la pantalla de Registro de Usuarios
class RegisterApp:
    # Constructor de la clase
    def __init__(self, page: ft.Page):
        self.page = page  # Guarda la referencia de la página
        self.show_password = False  # Estado para mostrar/ocultar contraseña
        self.show_confirm_password = False  # Estado para mostrar/ocultar confirmación de contraseña
        self.build()  # Construye la interfaz gráfica

    # Método que construye todos los elementos de la pantalla
    def build(self):
        # Campos de entrada de texto
        self.name = ft.TextField(label="Nombre Completo", width=300, height=50, dense=True)
        self.email = ft.TextField(label="Correo Electrónico", width=300, height=50, dense=True)
        self.username = ft.TextField(label="Usuario", width=300, height=50, dense=True)

        # Campo de contraseña con botón para mostrar/ocultar el contenido
        self.password = ft.TextField(
            label="Contraseña",
            password=True,  # Ocultar texto por defecto
            width=300,
            height=50,
            dense=True,
            suffix=ft.IconButton(  # Icono al final del campo
                icon=ft.Icons.VISIBILITY_OFF,
                on_click=self.toggle_password,  # Alternar visibilidad al hacer clic
            ),
        )

        # Campo para confirmar la contraseña con botón de mostrar/ocultar
        self.confirm_password = ft.TextField(
            label="Confirmar Contraseña",
            password=True,
            width=300,
            height=50,
            dense=True,
            suffix=ft.IconButton(
                icon=ft.Icons.VISIBILITY_OFF,
                on_click=self.toggle_confirm_password,  # Alternar visibilidad
            ),
        )

        # Botón principal para crear la cuenta
        register_button = ft.ElevatedButton(
            "Crear Cuenta",
            bgcolor="#43D9A2",  # Color verde agua
            color="#FFFFFF",  # Texto blanco
            style=ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(radius=20),  # Botón redondeado
                elevation=5,  # Sombra de botón
            ),
            width=220,
            height=45,
            on_click=self.confirm_register  # Antes de crear, confirma acción
        )

        # Botón de regreso al login
        back_button = ft.TextButton("Volver al Login", on_click=self.back_to_login)

        # Limpia la página y agrega los nuevos componentes
        self.page.controls.clear()
        self.page.add(
            ft.Column([
                ft.Text("Crear Cuenta", size=36, weight="bold", text_align="center"),  # Título principal
                ft.Container(height=5),  # Espaciador pequeño
                ft.Image(
                    src="assets/Cuenta.png",  # Imagen decorativa del registro
                    width=150,
                    height=150,
                    fit=ft.ImageFit.CONTAIN  # Ajuste proporcional
                ),
                ft.Container(height=10),  # Espaciador
                self.name,  # Campo nombre
                self.email,  # Campo email
                self.username,  # Campo usuario
                self.password,  # Campo contraseña
                self.confirm_password,  # Campo confirmar contraseña
                ft.Container(height=10),  # Espaciador
                register_button,  # Botón crear cuenta
                ft.Container(height=5),  # Espaciador
                back_button,  # Botón regresar
            ],
            alignment=ft.MainAxisAlignment.CENTER,  # Centrado vertical
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,  # Centrado horizontal
            spacing=10)  # Espaciado entre componentes
        )
        self.page.update()  # Actualiza la pantalla

    # Método para alternar visibilidad del campo de contraseña
    def toggle_password(self, e):
        self.show_password = not self.show_password  # Cambia el estado
        self.password.password = not self.show_password  # Cambia visibilidad
        self.password.suffix.icon = (
            ft.Icons.VISIBILITY if self.show_password else ft.Icons.VISIBILITY_OFF
        )  # Cambia el icono del botón
        self.page.update()

    # Método para alternar visibilidad del campo de confirmar contraseña
    def toggle_confirm_password(self, e):
        self.show_confirm_password = not self.show_confirm_password
        self.confirm_password.password = not self.show_confirm_password
        self.confirm_password.suffix.icon = (
            ft.Icons.VISIBILITY if self.show_confirm_password else ft.Icons.VISIBILITY_OFF
        )
        self.page.update()

    # Método para mostrar un cuadro de diálogo de confirmación antes de registrar
    def confirm_register(self, e):
        self.dialog = ft.AlertDialog(
            modal=True,  # No permite interactuar fuera del cuadro
            title=ft.Text("Confirmar Registro"),  # Título del cuadro
            content=ft.Text("¿Seguro que quieres crear la cuenta?"),  # Mensaje
            actions=[  # Botones de acción
                ft.TextButton("Cancelar", on_click=self.close_dialog),
                ft.TextButton("Sí, crear cuenta", on_click=self.register),
            ],
        )
        self.page.dialog = self.dialog
        self.dialog.open = True
        self.page.update()

    # Método para cerrar el cuadro de confirmación
    def close_dialog(self, e):
        self.dialog.open = False
        self.page.update()

    # Método que realiza el proceso de registro
    def register(self, e):

        print("🔔 register() llamado")
        print("Valores ➜",
          "nombre=", self.name.value,
          "email=", self.email.value,
          "usuario=", self.username.value,
          "pass=", self.password.value,
          "conf=", self.confirm_password.value)


        # Validaciones
        if not all([self.name.value,
                    self.email.value,
                    self.username.value,
                    self.password.value,
                    self.confirm_password.value]):
            print("⚠️ Campos incompletos")
            self.show_snackbar("Completa todos los campos.", "red")
            return

        if not self.is_valid_email(self.email.value):
            print("⚠️ Email inválido")
            self.show_snackbar("Correo electrónico no válido.", "red")
            return

        if self.password.value != self.confirm_password.value:
            print("⚠️ Contraseñas no coinciden")
            self.show_snackbar("Las contraseñas no coinciden.", "red")
            return

        try:
            coleccion = conectar_mongo()
            print("📡 Conexión a MongoDB OK:", coleccion.full_name if hasattr(coleccion, "full_name") else coleccion.name)
        except Exception as ex:
            print("❌ Error conectando a MongoDB:", ex)
            self.show_snackbar("Error de conexión a la base de datos.", "red")
            return

        try:
            existe = coleccion.find_one({"usuario": self.username.value.strip()})
            print("🔍 Usuario existente en BD?", bool(existe))
            if existe:
                self.show_snackbar("El usuario ya existe.", "red")
                return
        except Exception as ex:
            print("❌ Error al buscar usuario:", ex)
            self.show_snackbar("Error al verificar usuario.", "red")
            return

         # 5) Intentar insertar
        nuevo_usuario = {
            "nombre":          self.name.value.strip(),
            "correo":          self.email.value.strip(),
            "usuario":         self.username.value.strip(),
            "contraseña":      self.password.value.strip(),
            "fecha_registro":  time.strftime("%Y-%m-%dT%H:%M:%S")
         }
        try:
            resultado = coleccion.insert_one(nuevo_usuario)
            print("✅ Insertado _id:", resultado.inserted_id)
        except Exception as ex:
            print("❌ Error al insertar usuario:", ex)
            self.show_snackbar("Error al crear la cuenta.", "red")
            return

        # 6) Feedback al usuario y retorno al login
        self.show_snackbar("¡Cuenta creada exitosamente! 🎉", "green")
        # refrescamos UI
        self.page.update()

        from LoginApp import LoginApp
        self.page.controls.clear()
        LoginApp(self.page)


    # Método auxiliar para mostrar mensajes emergentes (snackbars)
    def show_snackbar(self, message, color):
        self.page.snack_bar = ft.SnackBar(
            content=ft.Text(message),
            bgcolor=color
        )
        self.page.snack_bar.open = True
        self.page.update()

    # Función que valida si un correo tiene formato correcto
    def is_valid_email(self, email):
        return bool(re.match(r"[^@]+@[^@]+\.[^@]+", email))  # Valida con expresión regular

    # Método para regresar a la pantalla de login
    def back_to_login(self, e):
        from LoginApp import LoginApp  # Importa la clase de login
        self.page.controls.clear()  # Limpia la página
        LoginApp(self.page)  # Llama a la clase de login
