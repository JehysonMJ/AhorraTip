import flet as ft
from datetime import datetime, timedelta
from LoginApp import conectar_mongo
from Sesion import usuario_actual
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import io, base64


def obtener_gastos_semana_actual():
    db = conectar_mongo()
    coleccion = db["gastos"]
    hoy = datetime.now()
    inicio_semana = hoy - timedelta(days=hoy.weekday())
    fin_semana = inicio_semana + timedelta(days=6)
    gastos = list(coleccion.find({
        "usuario": {"$regex": f"^{usuario_actual.strip()}$", "$options": "i"},
        "tipo": "GASTOS",
        "fecha": {"$gte": inicio_semana, "$lte": fin_semana}
    }))
    return gastos


def mostrar_grafico_y_lista():
    gastos = obtener_gastos_semana_actual()
    if not gastos:
        return ft.Text(
            "No hubo gastos esta semana", size=16, text_align="center"
        )

    # Agrupar por categoría
    resumen = {}
    for g in gastos:
        cat = g.get("categoria", "Sin categoría")
        resumen[cat] = resumen.get(cat, 0) + g.get("monto", 0)

    # Preparar datos para el gráfico
    labels = list(resumen.keys())
    sizes = list(resumen.values())

    # Crear figura y reducir márgenes
    fig, ax = plt.subplots(figsize=(4, 4), dpi=100)
    plt.subplots_adjust(left=0.01, right=0.99, top=0.99, bottom=0.01)

    # Generar pastel sin etiquetas, solo porcentajes
    wedges, texts, autotexts = ax.pie(
        sizes,
        autopct='%1.1f%%',
        startangle=90,
        pctdistance=0.6
    )
    # Ajustar estilo de porcentaje
    for t in autotexts:
        t.set_color('white')
        t.set_fontsize(10)

    ax.axis('equal')  # Mantener proporción circular

    # Guardar gráfico en memoria
    buf = io.BytesIO()
    fig.savefig(buf, format='png', bbox_inches='tight', transparent=True)
    plt.close(fig)
    buf.seek(0)
    img_b64 = base64.b64encode(buf.read()).decode('utf-8')

    # Devolver como imagen en Flet
    return ft.Image(
        src_base64=img_b64,
        width=320,
        height=320,
        fit=ft.ImageFit.CONTAIN
    )

class MainApp:
    def __init__(self, page: ft.Page):
        self.page = page
        self.build()

    def build(self):
        saludo = ft.Text(
            f"¡Bienvenido, {usuario_actual}!",
            size=20,
            weight="bold",
            color="white",
            text_align="center"
        )

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

        header = ft.Container(
            bgcolor="#2e7d32",
            padding=ft.padding.symmetric(horizontal=15, vertical=12),
            content=ft.Row([
                ft.IconButton(icon=ft.Icons.MENU, icon_color="white", on_click=lambda e: print("Menu")),
                ft.Column([
                    ft.Row([
                        ft.Icon(name=ft.Icons.SAVINGS, color="white", size=20),
                        ft.Text("Total", color="white", size=16)
                    ], alignment=ft.MainAxisAlignment.CENTER),
                    self.total_input
                ], alignment=ft.MainAxisAlignment.CENTER),
                ft.IconButton(icon=ft.Icons.RECEIPT_LONG, icon_color="white", on_click=lambda e: print("Historial"))
            ])
        )

        self.active_tab = "GASTOS"
        self.tab_gastos = ft.TextButton("GASTOS", on_click=self.set_tab, data="GASTOS")
        self.tab_ingresos = ft.TextButton("INGRESOS", on_click=self.set_tab, data="INGRESOS")

        period_selector = ft.Row([
            ft.TextButton("Día", on_click=self.change_period),
            ft.TextButton("Semana", on_click=self.change_period),
            ft.TextButton("Mes", on_click=self.change_period),
            ft.TextButton("Año", on_click=self.change_period)
        ], alignment=ft.MainAxisAlignment.CENTER)

        date_range = ft.Text("28 abr – 4 may", size=16, weight="bold")

        self.chart_container = ft.Container(
            content=mostrar_grafico_y_lista(),
            alignment=ft.alignment.center,
            width=320,
            height=320,
            bgcolor="#cfd8dc",
            border_radius=160
        )

        card = ft.Container(
            content=ft.Column([
                ft.Row([self.tab_gastos, self.tab_ingresos], alignment=ft.MainAxisAlignment.CENTER),
                period_selector,
                ft.Container(height=5),
                date_range,
                ft.Container(height=20),
                self.chart_container
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=10),
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
                card
            ], alignment=ft.MainAxisAlignment.START, horizontal_alignment=ft.CrossAxisAlignment.CENTER)
        )

        self.page.floating_action_button = ft.FloatingActionButton(
            icon=ft.Icons.ADD,
            bgcolor="#FFEB3B",
            on_click=self.add_transaction
        )
        self.page.update()

    def set_tab(self, e):
        self.active_tab = e.control.data
        self.actualizar_grafico()

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

    def actualizar_grafico(self):
        self.chart_container.content = mostrar_grafico_y_lista()
        self.page.update()
