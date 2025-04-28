# Importa la librería Flet para la creación de interfaces gráficas.
import flet as ft

# Función principal que define el contenido de la aplicación.
def main(page: ft.Page):
    # Configura propiedades de la página.
    page.title = "Control de Finanzas"  # Establece el título de la página.
    page.theme_mode = ft.ThemeMode.DARK  # Usa el modo oscuro.
    page.bgcolor = "#1b2a17"  # Define el color de fondo (verde oscuro).

    # Campo de texto editable para mostrar/modificar el total de dinero.
    total_field = ft.TextField(
        value="0",  # Valor inicial del campo (0).
        width=100,  # Ancho del campo en píxeles.
        text_align=ft.TextAlign.RIGHT,  # Alinea el texto a la derecha.
        border="none",  # Sin borde visible.
        bgcolor="transparent",  # Fondo transparente.
        text_style=ft.TextStyle(size=22, weight="bold"),  # Estilo de texto: tamaño 22 y negrita.
        height=40,  # Altura del campo en píxeles.
        dense=True,  # Reduce la separación vertical interna.
    )

    # Fila que agrupa el texto "Total ($)" junto al campo editable.
    total_row = ft.Row(
        [
            ft.Text("Total ($)", size=20),  # Texto "Total ($)" con tamaño de fuente 20.
            total_field,  # Campo de entrada del total.
        ],
        alignment=ft.MainAxisAlignment.CENTER,  # Centra los elementos horizontalmente.
        vertical_alignment=ft.CrossAxisAlignment.CENTER,  # Centra los elementos verticalmente.
        spacing=10,  # Espaciado de 10 píxeles entre los elementos.
    )

    # Barra superior que contiene el ícono de menú, el total y el ícono de recibo.
    top_bar = ft.Row(
        [
            ft.Icon(ft.icons.MENU, size=30),  # Ícono de menú (tamaño 30).
            total_row,  # Fila central con el total.
            ft.Icon(ft.icons.RECEIPT_LONG_OUTLINED, size=30),  # Ícono de recibo (tamaño 30).
        ],
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,  # Espacia los elementos entre sí.
        vertical_alignment=ft.CrossAxisAlignment.CENTER,  # Centra los elementos verticalmente.
    )

    # Tabs principales para alternar entre "GASTOS" e "INGRESOS".
    tabs = ft.Tabs(
        selected_index=0,  # El tab seleccionado inicialmente es "GASTOS".
        tabs=[
            ft.Tab(text="GASTOS"),  # Tab de "GASTOS".
            ft.Tab(text="INGRESOS"),  # Tab de "INGRESOS".
        ],
        expand=True,  # Los tabs se expanden para llenar el ancho disponible.
    )

    # Subtabs para filtrar los datos por períodos de tiempo.
    subtabs = ft.Row(
        [
            ft.Text("Día", style=ft.TextThemeStyle.BODY_MEDIUM),  # Texto para "Día".
            ft.Text("Semana", style=ft.TextThemeStyle.BODY_MEDIUM, weight="bold"),  # Texto para "Semana" en negritas.
            ft.Text("Mes", style=ft.TextThemeStyle.BODY_MEDIUM),  # Texto para "Mes".
            ft.Text("Año", style=ft.TextThemeStyle.BODY_MEDIUM),  # Texto para "Año".
            ft.Text("Período", style=ft.TextThemeStyle.BODY_MEDIUM),  # Texto para "Período".
        ],
        alignment=ft.MainAxisAlignment.SPACE_AROUND,  # Espacia los elementos de manera uniforme.
    )

    # Texto que muestra el rango de fechas actual (semana seleccionada).
    week_range = ft.Text("28 abr – 4 may", weight="bold", size=14)

    # Círculo que informa que no hubo gastos en la semana.
    circle = ft.Container(
        content=ft.Column(  # El contenido interno es una columna con tres textos.
            [
                ft.Text("No hubo", size=16),  # Primera línea: "No hubo".
                ft.Text("gastos esta", size=16),  # Segunda línea: "gastos esta".
                ft.Text("semana", size=16),  # Tercera línea: "semana".
            ],
            alignment=ft.MainAxisAlignment.CENTER,  # Centrado vertical de los textos.
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,  # Centrado horizontal de los textos.
        ),
        width=200,  # Ancho del contenedor (círculo) en píxeles.
        height=200,  # Altura del contenedor (círculo) en píxeles.
        bgcolor="#6c757d",  # Color de fondo gris.
        border_radius=100,  # Bordes redondeados para formar un círculo.
        alignment=ft.alignment.center,  # Centrado del círculo en el contenedor padre.
    )

    # Botón flotante que permite agregar un nuevo gasto.
    floating_button = ft.FloatingActionButton(
        icon=ft.icons.ADD,  # Ícono de suma (+).
        bgcolor="#FFD600",  # Color de fondo amarillo para el botón.
        on_click=lambda e: print("Agregar gasto"),  # Acción al hacer clic: imprime "Agregar gasto" en la consola.
    )

    # Agrega todos los componentes a la página principal en orden.
    page.add(
        top_bar,  # Agrega la barra superior con menú, total y recibo.
        tabs,  # Agrega los tabs principales "GASTOS" e "INGRESOS".
        subtabs,  # Agrega los subtabs de filtros por períodos de tiempo.
        week_range,  # Agrega el rango de fecha actual.
        ft.Container(content=circle, alignment=ft.alignment.center),  # Agrega el círculo informativo.
        floating_button,  # Agrega el botón flotante de agregar gasto.
    )

# Inicia la aplicación llamando a la función principal.
ft.app(target=main)
