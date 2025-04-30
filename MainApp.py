# Importa la librería Flet para crear interfaces gráficas
import flet as ft
from Sesion import usuario_actual  # ✅ Importar usuario logueado

# Clase principal de la aplicación
class MainApp:
    # Constructor que recibe la página principal
    def __init__(self, page: ft.Page):
        self.page = page  # Guarda la referencia de la página
        self.build()  # Llama a construir la interfaz

    # Método que arma toda la interfaz de la pantalla principal
    def build(self):
        # ✅ Saludo personalizado con el nombre del usuario
        saludo = ft.Text(f"Hola, {usuario_actual} 👋", size=20, weight="bold", color="white", text_align="center")

        # Campo de texto editable para el total
        self.total_input = ft.TextField(
            value="0",  # Valor inicial
            text_align=ft.TextAlign.CENTER,  # Texto centrado
            width=120,
            height=40,
            border_radius=10,  # Bordes redondeados
            border_color="transparent",  # Sin borde visible
            bgcolor="#FFFFFF",  # Fondo blanco
            color="#000000",  # Texto negro
            suffix_text="$",  # Símbolo de pesos al final
            on_change=self.total_updated  # Detecta cambios para mostrar notificación
        )

        # Encabezado superior
        header = ft.Container(
            bgcolor="#2e7d32",  # Verde oscuro
            padding=ft.padding.symmetric(horizontal=15, vertical=12),
            content=ft.Row([
                ft.IconButton(
                    icon=ft.icons.MENU,
                    icon_color="white",
                    on_click=lambda e: print("Abrir menú o ajustes"),
                    tooltip="Menú"
                ),
                ft.Column([
                    ft.Row([
                        ft.Icon(name=ft.icons.SAVINGS, color="white", size=20),
                        ft.Text("Total", color="white", size=16),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=5),
                    self.total_input
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                expand=1),
                ft.IconButton(
                    icon=ft.icons.RECEIPT_LONG,
                    icon_color="white",
                    on_click=lambda e: print("Ver historial o registros"),
                    tooltip="Historial"
                ),
            ])
        )

        self.active_tab = "GASTOS"
        self.tab_gastos = ft.TextButton("GASTOS", on_click=self.set_tab, data="GASTOS")
        self.tab_ingresos = ft.TextButton("INGRESOS", on_click=self.set_tab, data="INGRESOS")

        period_selector = ft.Row([
            ft.TextButton("Día", on_click=self.change_period),
            ft.TextButton("Semana", on_click=self.change_period),
            ft.TextButton("Mes", on_click=self.change_period),
            ft.TextButton("Año", on_click=self.change_period),
            ft.TextButton("Período", on_click=self.change_period),
        ], alignment=ft.MainAxisAlignment.CENTER)

        date_range = ft.Text("28 abr – 4 may", size=16, weight="bold")

        self.center_message = ft.Text(
            "No hubo gastos esta semana", size=16, text_align="center"
        )

        card = ft.Container(
            content=ft.Column([
                ft.Row([self.tab_gastos, self.tab_ingresos], alignment=ft.MainAxisAlignment.CENTER),
                period_selector,
                ft.Container(height=5),
                date_range,
                ft.Container(height=25),
                ft.Container(
                    content=self.center_message,
                    alignment=ft.alignment.center,
                    width=250,
                    height=250,
                    border_radius=125,
                    bgcolor="#cfd8dc"
                )
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=10),
            padding=20,
            bgcolor="#1e1e1e",
            border_radius=20,
            shadow=ft.BoxShadow(blur_radius=10, spread_radius=1, color="black")
        )

        # ✅ Agrega saludo arriba del header
        self.page.controls.clear()
        self.page.add(
            ft.Column([
                saludo,    # 👈 Saludo personalizado aquí
                header,
                ft.Container(height=20),
                card,
            ],
            alignment=ft.MainAxisAlignment.START,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=10)
        )
        self.page.update()

        floating_button = ft.FloatingActionButton(
            icon=ft.icons.ADD,
            bgcolor="#FFEB3B",
            shape=ft.CircleBorder(),
            tooltip="Agregar ingreso/gasto",
            on_click=self.add_transaction
        )

        self.page.floating_action_button = floating_button
        self.page.update()

    def set_tab(self, e):
        self.active_tab = e.control.data
        self.center_message.value = (
            "No hubo gastos esta semana" if self.active_tab == "GASTOS" else "No hubo ingresos esta semana"
        )
        self.page.update()

    def change_period(self, e):
        print(f"Período cambiado a: {e.control.text}")

    def total_updated(self, e):
        self.page.snack_bar = ft.SnackBar(
            content=ft.Text(f"Monto actualizado: ${self.total_input.value}"),
            bgcolor="#43A047",
            duration=1500
        )
        self.page.snack_bar.open = True
        self.page.update()

    def add_transaction(self, e):
        from NuevaTransaccion import AddTransactionApp
        self.page.controls.clear()
        AddTransactionApp(self.page)
