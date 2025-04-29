import flet as ft
import time
import threading
from LoginApp import LoginApp

class SplashScreenApp:
    def __init__(self, page: ft.Page):
        self.page = page
        self.page.bgcolor = "#1e1e1e"  # Fondo oscuro original
        self.page.theme_mode = ft.ThemeMode.DARK
        self.page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
        self.page.vertical_alignment = ft.MainAxisAlignment.CENTER

        # Logo con animaciones configuradas
        self.logo = ft.Image(
            src="assets/LogoAhorraTip.png",
            width=200,
            height=200,
            animate_offset=True,
            animate_opacity=300,
            opacity=1.0,
            offset=ft.Offset(0, 0)
        )

        self.page.clean()
        self.page.add(self.logo)
        self.page.update()

        # Lanzamos animación en un hilo aparte
        threading.Thread(target=self.animate_and_transition).start()

    def animate_and_transition(self):
        time.sleep(1.5)

        # Desliza el logo hacia abajo y lo desvanece
        self.logo.offset = ft.Offset(0, 2)
        self.logo.opacity = 0.0
        self.page.update()

        time.sleep(1.0)
        self.page.controls.clear()
        LoginApp(self.page)
