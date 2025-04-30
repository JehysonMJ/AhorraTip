# Importaciones necesarias
import flet as ft  # Flet para construir interfaces gráficas
import time  # Para controlar pausas (tiempo entre animaciones)
import threading  # Para correr animaciones sin bloquear la interfaz
from LoginApp import LoginApp  # Importa la pantalla de login

# Clase principal de la pantalla de presentación (Splash Screen)
class SplashScreenApp:
    def __init__(self, page: ft.Page):
        self.page = page  # Guarda la referencia de la página actual

        # Configura el fondo y modo de tema de la página
        self.page.bgcolor = "#1e1e1e"  # Fondo oscuro
        self.page.theme_mode = ft.ThemeMode.DARK  # Modo oscuro activado
        self.page.horizontal_alignment = ft.CrossAxisAlignment.CENTER  # Alineación horizontal centrada
        self.page.vertical_alignment = ft.MainAxisAlignment.CENTER  # Alineación vertical centrada

        # Imagen del logo con animaciones
        self.logo = ft.Image(
            src="assets/LogoAhorraTip.png",  # Ruta de la imagen del logo
            width=200,
            height=200,
            fit=ft.ImageFit.CONTAIN,  # Ajuste proporcional
            animate_offset=True,  # Habilita animación de posición
            animate_opacity=300,  # Habilita animación de opacidad (300ms)
            opacity=1.0,  # Totalmente visible al inicio
            offset=ft.Offset(0, 0)  # Posición inicial (centro)
        )

        # Texto de carga con animaciones
        self.texto = ft.Text(
            value="Cargando AhorraTip...",  # Texto mostrado al usuario
            size=18,
            color="white",
            opacity=1.0,  # Visible al inicio
            offset=ft.Offset(0, 0),  # Posición inicial
            animate_opacity=300,
            animate_offset=True
        )

        # Limpia la página y agrega los elementos
        self.page.clean()
        self.page.add(
            ft.Column([
                self.logo,   # Imagen del logo
                self.texto   # Texto de carga
            ],
            alignment=ft.MainAxisAlignment.CENTER,  # Centrado vertical
            horizontal_alignment=ft.CrossAxisAlignment.CENTER)  # Centrado horizontal
        )
        self.page.update()  # Aplica los cambios visuales

        # Lanza la animación en un hilo separado para no congelar la interfaz
        threading.Thread(target=self.animate_and_transition).start()

    # Método que anima el contenido y luego cambia a la pantalla de login
    def animate_and_transition(self):
        time.sleep(1.5)  # Espera 1.5 segundos antes de empezar la animación de salida

        # Anima el logo y el texto hacia abajo y desvanece
        self.logo.offset = ft.Offset(0, 2)  # Mueve el logo hacia abajo
        self.logo.opacity = 0.0  # Lo desvanece
        self.texto.offset = ft.Offset(0, 2)  # Mueve el texto hacia abajo
        self.texto.opacity = 0.0  # Lo desvanece
        self.page.update()  # Aplica las animaciones

        time.sleep(1.0)  # Espera 1 segundo más antes de cambiar de pantalla

        # Limpia los controles y muestra la pantalla de Login
        self.page.controls.clear()
        LoginApp(self.page)  # Llama a la clase de login
