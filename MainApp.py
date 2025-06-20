import flet as ft
from flet import ScrollMode
from datetime import datetime, timedelta
from LoginApp import conectar_mongo
from Sesion import usuario_actual
import matplotlib
matplotlib.use('Agg')   # Evita el uso de GUI para renderizado
import matplotlib.pyplot as plt
import io, base64

# Colores por defecto de Matplotlib para usar en el pie y leyenda
DEFAULT_COLORS = plt.rcParams['axes.prop_cycle'].by_key()['color']

# Función genérica para obtener transacciones (GASTOS o INGRESOS) de la semana actual
def obtener_transacciones_semana_actual(tipo: str):
    db = conectar_mongo()
    coleccion = db["gastos"] if tipo == "GASTOS" else db["ingresos"]
    hoy = datetime.now()
    inicio_semana = hoy - timedelta(days=hoy.weekday())    # Lunes
    fin_semana = inicio_semana + timedelta(days=6)          # Domingo
    return list(coleccion.find({
        "usuario": {"$regex": f"^{usuario_actual.strip()}$", "$options": "i"},
        "tipo": tipo,
        "fecha": {"$gte": inicio_semana, "$lte": fin_semana}
    }))

# Función que construye el gráfico circular y lo muestra como imagen
def mostrar_grafico_y_lista(tipo: str):
    transacciones = obtener_transacciones_semana_actual(tipo)
    if not transacciones:
        return ft.Text(f"No hubo {tipo.lower()} esta semana", size=16, text_align="center")

    # Agrupa montos por categoría
    resumen = {}
    for t in transacciones:
        cat = t.get("categoria", "Sin categoría")
        resumen[cat] = resumen.get(cat, 0) + t.get("monto", 0)
    labels = list(resumen.keys())
    sizes = list(resumen.values())
    colors = DEFAULT_COLORS[:len(labels)]

    # Crea el gráfico circular
    fig, ax = plt.subplots(figsize=(4, 4), dpi=100)
    plt.subplots_adjust(left=0.01, right=0.99, top=0.99, bottom=0.01)
    wedges, texts, autotexts = ax.pie(
        sizes,
        labels=None,
        autopct='%1.1f%%',
        startangle=90,
        pctdistance=0.6,
        colors=colors
    )
    for t in autotexts:
        t.set_color('white')
        t.set_fontsize(10)
    ax.axis('equal')    # Mantiene el gráfico como círculo

    ## Convierte la imagen en base64 para mostrarla en Flet
    buf = io.BytesIO()
    fig.savefig(buf, format='png', bbox_inches='tight', transparent=True)
    plt.close(fig)
    buf.seek(0)
    img_b64 = base64.b64encode(buf.read()).decode('utf-8')
    buf.close()

    return ft.Image(src_base64=img_b64, width=320, height=320, fit=ft.ImageFit.CONTAIN)

# Clase principal de la aplicación después del login
class MainApp:
    def __init__(self, page: ft.Page):
        # Guarda la referencia de la página Flet
        self.page = page
        
       # Menú de navegación lateral
        self.page.on_navigation_drawer_change = self.navegar_menu
        self.page.navigation_drawer = ft.NavigationDrawer(
            controls=[
                ft.NavigationDrawerDestination(icon=ft.Icons.PERSON,       label="Perfil de usuario"),
                ft.NavigationDrawerDestination(icon=ft.Icons.DARK_MODE,    label="Modo oscuro"),
                ft.Divider(),
                ft.NavigationDrawerDestination(icon=ft.Icons.SETTINGS,     label="Configuración"),
                ft.NavigationDrawerDestination(icon=ft.Icons.LOGOUT,       label="Cerrar sesión"),
            ]
        )
        # Y el scroll
        self.page.vertical_scroll = ScrollMode.AUTO  # Habilita scroll vertical automático

        # Tab por defecto
        self.active_tab = "GASTOS"

        # Construye la interfaz inicial
        self.build()

    # Construye toda la interfaz principal
    def build(self):
        # Mensaje de bienvenida
        saludo = ft.Text(
            f"¡Bienvenido, {usuario_actual}!",
            size=20, weight="bold", color="white", text_align="center"
        )

         # Campo editable del total
        self.total_input = ft.TextField(
            value="0", text_align=ft.TextAlign.CENTER,
            width=120, height=40, border_radius=10,
            border_color="transparent", bgcolor="#FFFFFF",
            color="#000000", suffix_text="$",
            on_change=self.total_updated
        )

        # Encabezado con íconos y total
        header = ft.Container(
            bgcolor="#2e7d32",
            padding=ft.padding.symmetric(horizontal=15, vertical=12),
            content=ft.Row([
                ft.IconButton(icon=ft.Icons.MENU, icon_color="white", on_click=self.open_drawer),
                ft.Column([
                    ft.Row([
                        ft.Icon(name=ft.Icons.SAVINGS, color="white", size=20),
                        ft.Text("Total", color="white", size=16),
                    ], alignment=ft.MainAxisAlignment.CENTER),
                    ft.Row([self.total_input], alignment=ft.MainAxisAlignment.CENTER)
                ], expand=True, alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                ft.IconButton(icon=ft.Icons.RECEIPT_LONG, icon_color="white", on_click=lambda e: print("Historial")),
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN, vertical_alignment=ft.CrossAxisAlignment.CENTER)
        )

        # Tabs para GASTOS e INGRESOS
        self.tab_gastos = ft.TextButton("GASTOS", on_click=self.set_tab, data="GASTOS")
        self.tab_ingresos = ft.TextButton("INGRESOS", on_click=self.set_tab, data="INGRESOS")

        # Selector de período (aún no implementado completamente)
        period_selector = ft.Row([
            ft.TextButton("Día", on_click=self.change_period),
            ft.TextButton("Semana", on_click=self.change_period),
            ft.TextButton("Mes", on_click=self.change_period),
            ft.TextButton("Año", on_click=self.change_period),
        ], alignment=ft.MainAxisAlignment.CENTER)

        date_range = ft.Text("28 abr – 4 may", size=16, weight="bold")

        # Contenedor para el gráfico generado
        self.chart_container = ft.Container(
            content=mostrar_grafico_y_lista(self.active_tab),
            alignment=ft.alignment.center,
            width=320, height=320, bgcolor="#cfd8dc", border_radius=160
        )

        # Texto con el total gastado/ingresado
        resumen_inicial = self.obtener_resumen()
        total_value = sum(resumen_inicial.values())
        prefijo = "gastado" if self.active_tab == "GASTOS" else "ingresado"
        self.total_spent_text = ft.Text(
            f"Total {prefijo}: ${total_value:,.2f}",
            color="white", weight="bold", size=16, text_align="center"
        )

        # Contenedor para el resumen por categoría
        self.summary_container = ft.Column(spacing=6)
        self.update_resumen()

        # Tarjeta central con toda la información de la semana
        card = ft.Container(
            content=ft.Column([
                ft.Row([self.tab_gastos, self.tab_ingresos], alignment=ft.MainAxisAlignment.CENTER),
                period_selector,
                ft.Container(height=5),
                ft.Row([date_range], alignment=ft.MainAxisAlignment.CENTER),
                ft.Container(height=20),
                ft.Row([self.chart_container], alignment=ft.MainAxisAlignment.CENTER),
                ft.Row([self.total_spent_text], alignment=ft.MainAxisAlignment.CENTER),
                ft.Container(height=15),
                ft.Text(f"Resumen de {self.active_tab.lower()} por categoría:", color="white", weight="bold"),
                self.summary_container
            ], spacing=10),
            padding=20, bgcolor="#1e1e1e", border_radius=20,
            shadow=ft.BoxShadow(blur_radius=10, spread_radius=1, color="black")
        )

        # Agrega todo a la página principal
        self.page.controls.clear()
        self.page.add(
            ft.ListView(
                expand=1, spacing=20, padding=20, auto_scroll=True,
                controls=[saludo, header, card]
            )
        )

         # Botón flotante para agregar una nueva transacción
        self.page.floating_action_button = ft.FloatingActionButton(
            icon=ft.Icons.ADD, bgcolor="#FFEB3B", on_click=self.add_transaction
        )
        self.page.update()

    # Abre el menú de navegación lateral
    def open_drawer(self, e):
        self.page.show_navigation_drawer = True
        self.page.update()

    # Placeholder para navegación a perfil
    def on_profile(self, e):
        print("Navegar a Perfil de usuario")  # implementar navegación

    # Alterna entre modo claro y oscuro
    def on_toggle_dark_mode(self, e):
        self.page.theme_mode = ft.ThemeMode.DARK if self.page.theme_mode == ft.ThemeMode.LIGHT else ft.ThemeMode.LIGHT
        self.page.update()

    # Placeholder para navegación a configuración
    def on_settings(self, e):
        print("Navegar a Configuración")  # implementar navegación

    # Placeholder para cerrar sesión
    def on_logout(self, e):
        print("Cerrar sesión")  # implementar lógica de cierre de sesión

    # Calcula el total por categoría
    def obtener_resumen(self):
        resumen = {}
        for t in obtener_transacciones_semana_actual(self.active_tab):
            cat = t.get("categoria", "Sin categoría")
            resumen[cat] = resumen.get(cat, 0) + t.get("monto", 0)
        return resumen

    # Actualiza la lista resumen de categorías
    def update_resumen(self):
        resumen = self.obtener_resumen()
        controles = []
        for i, (cat, monto) in enumerate(resumen.items()):
            color = DEFAULT_COLORS[i % len(DEFAULT_COLORS)]
            controles.append(
                ft.Row([
                    ft.Container(width=12, height=12, bgcolor=color, border_radius=3, margin=ft.margin.only(right=8)),
                    ft.Text(cat, color="white", expand=True),
                    ft.Text(f"${monto:,.2f}", color="white")
                ])
            )
        if not controles:
            controles = [ft.Text(f"No hay {self.active_tab.lower()} para mostrar.", color="white")]
        self.summary_container.controls = controles

    # Cambia entre las tabs de GASTOS / INGRESOS
    def set_tab(self, e):
        self.active_tab = e.control.data
        self.chart_container.content = mostrar_grafico_y_lista(self.active_tab)
        self.update_resumen()
        total_value = sum(self.obtener_resumen().values())
        prefijo = "gastado" if self.active_tab == "GASTOS" else "ingresado"
        self.total_spent_text.value = f"Total {prefijo}: ${total_value:,.2f}"
        self.page.update()

    # Evento para cambiar el período (por ahora solo imprime)
    def change_period(self, e):
        print(f"Período cambiado a: {e.control.text}")

     # Evento cuando se cambia el valor del total
    def total_updated(self, e):
        self.page.snack_bar = ft.SnackBar(
            content=ft.Text(f"Monto actualizado: ${self.total_input.value}"),
            bgcolor="#43A047", duration=1500
        )
        self.page.snack_bar.open = True
        self.page.update()

     # Navega a la pantalla de nueva transacción
    def add_transaction(self, e):
        from NuevaTransaccion import AddTransactionApp
        self.page.controls.clear()
        AddTransactionApp(self.page, self)
        self.page.update()

    # Método externo que actualiza el gráfico y el resumen
    def actualizar_grafico(self):
        self.chart_container.content = mostrar_grafico_y_lista(self.active_tab)
        total_value = sum(self.obtener_resumen().values())
        prefijo = "gastado" if self.active_tab == "GASTOS" else "ingresado"
        self.total_spent_text.value = f"Total {prefijo}: ${total_value:,.2f}"
        self.update_resumen()
        self.page.update()
        
    # Maneja la navegación del menú lateral
    def navegar_menu(self, e):
        label = e.control.label
        if label == "Perfil de usuario":
            self.on_profile(e)
        elif label == "Modo oscuro":
            self.on_toggle_dark_mode(e)
        elif label == "Configuración":
            self.on_settings(e)
        elif label == "Cerrar sesión":
            self.on_logout(e)

