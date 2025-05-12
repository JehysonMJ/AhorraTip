import flet as ft
from datetime import datetime, timedelta
from LoginApp import conectar_mongo
from Sesion import usuario_actual

def obtener_gastos_semana_actual():
    db = conectar_mongo()
    coleccion = db["gastos"]
    hoy = datetime.now()
    inicio_semana = hoy - timedelta(days=hoy.weekday())
    fin_semana = inicio_semana + timedelta(days=6)
    gastos = list(coleccion.find({
        "usuario": {"$regex": f"^{usuario_actual.strip()}$", "$options": "i"},  # Búsqueda insensible a mayúsculas y sin espacios
        "tipo": "GASTOS",
        "fecha": {
            "$gte": inicio_semana,
            "$lte": fin_semana
        }
    }))
    return gastos

def mostrar_grafico_y_lista():
    gastos = obtener_gastos_semana_actual()
    if not gastos:
        return ft.Text("No hubo gastos esta semana", size=16, text_align="center")

    total = sum(g["monto"] for g in gastos)
    resumen = {}
    for g in gastos:
        cat = g["categoria"]
        resumen[cat] = resumen.get(cat, 0) + g["monto"]

    grafico = ft.Text(f"{round(total)} $", size=28, weight="bold", text_align="center")

    lista_detalles = [
        ft.Row([
            ft.Text(cat, expand=1),
            ft.Text(f"{round((monto/total)*100)} %"),
            ft.Text(f"{monto:.0f} $")
        ]) for cat, monto in resumen.items()
    ]

    return ft.Column([
        ft.Container(content=grafico, alignment=ft.alignment.center, width=200, height=200, bgcolor="#cfd8dc", border_radius=100),
        ft.Column(lista_detalles, spacing=5)
    ],
    alignment=ft.MainAxisAlignment.CENTER,
    horizontal_alignment=ft.CrossAxisAlignment.CENTER)

class MainApp:
    def __init__(self, page: ft.Page):
        self.page = page
        self.build()

    def build(self):
        # ✅ Saludo personalizado con el nombre del usuario
        saludo = ft.Text(f"¡Bienvenido, {usuario_actual} !", size=20, weight="bold", color="white", text_align="center")

        # Campo de texto editable para el total
        self.total_input = ft.TextField(
            value="0",
            text_align=ft.TextAlign.CENTER,
            width=120,
            height=40,
            border_radius=10,
            border_color="transparent",
            bgcolor="#FFFFFF",
            color="#000000",
            suffix_text="$",
            on_change=self.total_updated
        )

        # Encabezado superior
        header = ft.Container(
            bgcolor="#2e7d32",
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

        # ✅ Aquí definimos correctamente el container dinámico
        self.center_message_container = ft.Container(
            content=mostrar_grafico_y_lista(),
            alignment=ft.alignment.center,
            width=250,
            height=250,
            border_radius=125,
            bgcolor="#cfd8dc"
        )

        card = ft.Container(
            content=ft.Column([
                ft.Row([self.tab_gastos, self.tab_ingresos], alignment=ft.MainAxisAlignment.CENTER),
                period_selector,
                ft.Container(height=5),
                date_range,
                ft.Container(height=25),
                self.center_message_container  # ✅ Usamos el container dinámico aquí
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=10),
            padding=20,
            bgcolor="#1e1e1e",
            border_radius=20,
            shadow=ft.BoxShadow(blur_radius=10, spread_radius=1, color="black")
        )

        self.page.controls.clear()
        self.page.add(
            ft.Column([
                saludo,
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
        self.actualizar_grafico()  # 🔁 Actualiza la gráfica según pestaña
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

    # 🔁 Nueva función para actualizar el gráfico y lista
    def actualizar_grafico(self):
        self.center_message_container.content = mostrar_grafico_y_lista()
        self.page.update()
