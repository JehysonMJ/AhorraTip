# Importa la librería Flet para crear interfaces gráficas
import flet as ft

# Clase principal de la aplicación
class MainApp:
    # Constructor que recibe la página principal
    def __init__(self, page: ft.Page):
        self.page = page  # Guarda la referencia de la página
        self.build()  # Llama a construir la interfaz

    # Método que arma toda la interfaz de la pantalla principal
    def build(self):
        # Campo de texto editable para el total
        self.total_input = ft.TextField(
            value="1870",  # Valor inicial
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

        # Encabezado superior que contiene menú, total y botón de historial
        header = ft.Container(
            bgcolor="#2e7d32",  # Verde oscuro
            padding=ft.padding.symmetric(horizontal=15, vertical=12),  # Espaciado interno
            content=ft.Row([
                # Botón de menú
                ft.IconButton(
                    icon=ft.icons.MENU,
                    icon_color="white",
                    on_click=lambda e: print("Abrir menú o ajustes"),
                    tooltip="Menú"
                ),
                # Columna central con ícono de ahorro, texto "Total" y campo editable
                ft.Column([
                    ft.Row([
                        ft.Icon(name=ft.icons.SAVINGS, color="white", size=20),
                        ft.Text("Total", color="white", size=16),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=5),
                    self.total_input  # Campo editable
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                expand=1),
                # Botón de historial
                ft.IconButton(
                    icon=ft.icons.RECEIPT_LONG,
                    icon_color="white",
                    on_click=lambda e: print("Ver historial o registros"),
                    tooltip="Historial"
                ),
            ])
        )

        # Pestañas de navegación: Gastos e Ingresos
        self.active_tab = "GASTOS"  # Pestaña activa inicialmente
        self.tab_gastos = ft.TextButton("GASTOS", on_click=self.set_tab, data="GASTOS")
        self.tab_ingresos = ft.TextButton("INGRESOS", on_click=self.set_tab, data="INGRESOS")

        # Selector de periodo de tiempo
        period_selector = ft.Row([
            ft.TextButton("Día", on_click=self.change_period),
            ft.TextButton("Semana", on_click=self.change_period),
            ft.TextButton("Mes", on_click=self.change_period),
            ft.TextButton("Año", on_click=self.change_period),
            ft.TextButton("Período", on_click=self.change_period),
        ], alignment=ft.MainAxisAlignment.CENTER)

        # Texto de fecha de la semana seleccionada
        date_range = ft.Text("28 abr – 4 may", size=16, weight="bold")

        # Mensaje central que cambia según la pestaña activa
        self.center_message = ft.Text(
            "No hubo gastos esta semana", size=16, text_align="center"
        )

        # Tarjeta central que agrupa todo: tabs, periodo, fecha y mensaje
        card = ft.Container(
            content=ft.Column([
                ft.Row([self.tab_gastos, self.tab_ingresos], alignment=ft.MainAxisAlignment.CENTER),
                period_selector,
                ft.Container(height=5),  # Separador pequeño
                date_range,
                ft.Container(height=25),  # Separador grande
                ft.Container(
                    content=self.center_message,
                    alignment=ft.alignment.center,
                    width=250,
                    height=250,
                    border_radius=125,  # Para que sea un círculo
                    bgcolor="#cfd8dc"  # Fondo gris claro
                )
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=10),
            padding=20,
            bgcolor="#1e1e1e",  # Fondo de la tarjeta oscuro
            border_radius=20,  # Bordes redondeados
            shadow=ft.BoxShadow(blur_radius=10, spread_radius=1, color="black")  # Sombra
        )

        # Limpia controles actuales y agrega los nuevos
        self.page.controls.clear()
        self.page.add(
            ft.Column([
                header,  # Agrega el encabezado
                ft.Container(height=20),  # Espaciador
                card,  # Agrega la tarjeta central
            ],
            alignment=ft.MainAxisAlignment.START,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=10)
        )
        self.page.update()

        # Botón flotante amarillo para agregar nueva transacción
        floating_button = ft.FloatingActionButton(
            icon=ft.icons.ADD,  # Ícono "+"
            bgcolor="#FFEB3B",  # Color amarillo
            shape=ft.CircleBorder(),  # Forma de círculo
            tooltip="Agregar ingreso/gasto",  # Texto flotante
            on_click=self.add_transaction  # Acción al hacer clic
        )

        # Asigna el botón flotante a la página
        self.page.floating_action_button = floating_button
        self.page.update()

    # Método para cambiar entre pestañas (GASTOS o INGRESOS)
    def set_tab(self, e):
        self.active_tab = e.control.data  # Cambia la pestaña activa
        # Actualiza el mensaje central según la pestaña
        self.center_message.value = (
            "No hubo gastos esta semana" if self.active_tab == "GASTOS" else "No hubo ingresos esta semana"
        )
        self.page.update()

    # Método que responde al cambiar el periodo (día, semana, mes, año)
    def change_period(self, e):
        print(f"Período cambiado a: {e.control.text}")  # Imprime en consola el periodo elegido

    # Método que muestra una notificación al cambiar el total
    def total_updated(self, e):
        self.page.snack_bar = ft.SnackBar(
            content=ft.Text(f"Monto actualizado: ${self.total_input.value}"),  # Mensaje dinámico
            bgcolor="#43A047",  # Verde
            duration=1500  # Dura 1.5 segundos
        )
        self.page.snack_bar.open = True
        self.page.update()

    # Método para simular la adición de una nueva transacción
    def add_transaction(self, e):
        from NuevaTransaccion import AddTransactionApp  # Importa el módulo de nueva transacción
        self.page.controls.clear()  # Limpia la pantalla actual
        AddTransactionApp(self.page)  # Carga la nueva pantalla
