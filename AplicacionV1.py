# Versión Inicial, solo una muestra de lo que se tiene planeado.
import flet as ft  # Importamos la librería Flet para construir la interfaz de usuario.

# Función principal que configura la página.
def main(page: ft.Page):
    page.title = "Control de Finanzas"  # Establece el título de la página.
    page.theme_mode = ft.ThemeMode.DARK  # Activa el modo oscuro para la aplicación.
    page.bgcolor = "#1b2a17"  # Define el color de fondo como verde oscuro.

    # Encabezado superior con íconos y textos (Total e importe).
    header = ft.Row(
        [
            ft.Icon(ft.icons.MENU),  # Ícono de menú.
            ft.Text("Total", size=16),  # Texto "Total" con tamaño 16.
            ft.Text("1,870 $", weight="bold", size=24),  # Monto total en negritas y tamaño 24.
            ft.Icon(ft.icons.RECEIPT_LONG_OUTLINED),  # Ícono de recibo largo.
        ],
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,  # Alinea los elementos con espacio entre ellos.
    )

    # Tabs principales para alternar entre "Gastos" e "Ingresos".
    tabs = ft.Tabs(
        selected_index=0,  # Define el tab seleccionado inicialmente (Gastos).
        tabs=[
            ft.Tab(text="GASTOS"),  # Tab para la sección de gastos.
            ft.Tab(text="INGRESOS"),  # Tab para la sección de ingresos.
        ],
        expand=True,  # Los tabs ocupan todo el espacio horizontal disponible.
    )

    # Subtabs para filtrar la información por tiempo (Día, Semana, Mes, Año, Período).
    subtabs = ft.Row(
        [
            ft.Text("Día", style=ft.TextThemeStyle.BODY_MEDIUM),  # Texto para Día.
            ft.Text("Semana", style=ft.TextThemeStyle.BODY_MEDIUM, weight="bold"),  # Texto para Semana (en negritas).
            ft.Text("Mes", style=ft.TextThemeStyle.BODY_MEDIUM),  # Texto para Mes.
            ft.Text("Año", style=ft.TextThemeStyle.BODY_MEDIUM),  # Texto para Año.
            ft.Text("Período", style=ft.TextThemeStyle.BODY_MEDIUM),  # Texto para Período.
        ],
        alignment=ft.MainAxisAlignment.SPACE_AROUND,  # Alinea los textos distribuidos uniformemente.
    )

    # Texto que muestra el rango de la semana actual.
    week_range = ft.Text("28 abr – 4 may", weight="bold", size=14)

    # Contenedor circular que muestra un mensaje cuando no hay gastos.
    circle = ft.Container(
        content=ft.Column(  # El contenido del círculo es una columna de textos.
            [
                ft.Text("No hubo", size=16),  # Texto "No hubo" con tamaño 16.
                ft.Text("gastos esta", size=16),  # Texto "gastos esta" con tamaño 16.
                ft.Text("semana", size=16),  # Texto "semana" con tamaño 16.
            ],
            alignment=ft.MainAxisAlignment.CENTER,  # Centra los textos verticalmente.
            horizontal_alignment=ft.CrossAxisAlignment.CENTER  # Centra los textos horizontalmente.
        ),
        width=200,  # Ancho del contenedor.
        height=200,  # Alto del contenedor.
        bgcolor="#6c757d",  # Color de fondo gris.
        border_radius=100,  # Borde redondeado para formar un círculo perfecto.
        alignment=ft.alignment.center,  # Centra el contenedor en su espacio.
    )

    # Botón flotante para agregar un nuevo gasto.
    floating_button = ft.FloatingActionButton(
        icon=ft.icons.ADD,  # Ícono de suma (+).
        bgcolor="#FFD600",  # Color de fondo amarillo.
        on_click=lambda e: print("Agregar gasto"),  # Acción al hacer clic: imprime un mensaje en consola.
    )

    # Agrega todos los componentes a la página en orden.
    page.add(
        header,  # Agrega el encabezado.
        tabs,  # Agrega los tabs principales.
        subtabs,  # Agrega los subtabs de tiempo.
        week_range,  # Agrega el rango de fechas.
        ft.Container(content=circle, alignment=ft.alignment.center),  # Agrega el círculo con mensaje.
        floating_button,  # Agrega el botón flotante.
    )

# Ejecuta la aplicación llamando a la función principal.
ft.app(target=main)
