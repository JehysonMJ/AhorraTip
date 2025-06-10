# Importa la librería Flet y la clase AddTransactionApp
import flet as ft
from NuevaTransaccion import AddTransactionApp  # Importa la pantalla para añadir transacciones

# Clase que representa la pantalla para elegir una nueva categoría
class NuevaCategoria:
    def __init__(self, page: ft.Page, main_app):
        self.page = page  # Guarda la referencia a la página
        self.main_app = main_app
        self.build()  # Llama al método que construye la interfaz

    # Método que construye toda la pantalla de selección de categorías
    def build(self):
        # Lista de categorías disponibles: (emoji, nombre, color)
        categorias = [
            ("❤️", "Salud", "#e53935"), ("💳", "Ocio", "#43a047"), ("🏠", "Casa", "#1e88e5"), ("☕", "Café", "#fdd835"),
            ("🎓", "Educación", "#ab47bc"), ("🎁", "Regalos", "#aed581"), ("🛒", "Alimentación", "#4fc3f7"), ("👨‍👩‍👧", "Familia", "#ef5350"),
            ("💪", "Rutina", "#66bb6a"), ("🚌", "Transporte", "#42a5f5"), ("❓", "Otros", "#ef5350"), ("👟", "Ropa", "#ec407a"),
            ("🎮", "Diversion", "#fbc02d"), ("🚗", "Vehiculo", "#f06292"), ("📱", "Telefono", "#ce93d8"),
            ("💇", "Fisico", "#4dd0e1"), ("🐖", "Ahorro", "#212121"), ("🤝", "Deposito", "#b39ddb"),
        ]

        chips = []  # Lista de filas completas de chips (categorías visuales)
        row = []  # Fila temporal para acumular chips de 4 en 4

        # Genera un chip (ícono redondo + nombre) para cada categoría
        for i, (emoji, nombre, color) in enumerate(categorias):
            chip = ft.GestureDetector(  # Permite detectar clics sobre el chip
                on_tap=lambda e, cat=nombre: self.return_to_transaction(cat),  # Al hacer clic, vuelve con la categoría elegida
                content=ft.Container(
                    content=ft.Column([
                        # Contenedor circular con el emoji
                        ft.Container(
                            content=ft.Text(emoji, size=22),
                            width=60,
                            height=60,
                            bgcolor=color,
                            border_radius=30,
                            alignment=ft.alignment.center
                        ),
                        # Texto debajo del emoji con el nombre de la categoría
                        ft.Text(nombre, size=12, text_align="center", color="#FFFFFF")
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                    padding=5,
                    width=70
                )
            )
            row.append(chip)

            # Agrupa cada 4 chips en una fila
            if (i + 1) % 4 == 0:
                chips.append(ft.Row(row, alignment=ft.MainAxisAlignment.CENTER, spacing=20))
                row = []

        # Si quedó alguna categoría fuera (menos de 4), la agrega en la última fila
        if row:
            chips.append(ft.Row(row, alignment=ft.MainAxisAlignment.CENTER, spacing=20))

        # Botón para volver sin seleccionar categoría
        back_button = ft.TextButton("← Volver", on_click=self.go_back)

        # Limpia los controles anteriores y arma la pantalla con las categorías
        self.page.controls.clear()
        self.page.add(
            ft.Column([
                ft.Text("Selecciona una categoría", size=28, weight="bold"),  # Título de pantalla
                ft.Column(chips, spacing=20),  # Todas las filas de chips
                back_button  # Botón de regreso
            ],
            alignment=ft.MainAxisAlignment.START,  # Alineación vertical
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,  # Alineación horizontal
            spacing=20,  # Espaciado entre elementos
            scroll=ft.ScrollMode.AUTO)  # Scroll si se excede la altura
        )
        self.page.update()

    # Método que regresa a la pantalla de transacciones con la categoría seleccionada
    def return_to_transaction(self, categoria_seleccionada):
        self.page.controls.clear()  # Limpia la pantalla
        app = AddTransactionApp(self.page, self.main_app)  # Crea instancia de la pantalla de transacción
        app.selected_category = categoria_seleccionada  # Asigna la categoría seleccionada
        app.amount_field.value = ""  # Limpia el campo de monto
        app.comment_field.value = ""  # Limpia el campo de comentario
        app.build()  # Reconstruye la pantalla con la categoría preseleccionada

    # Método para regresar sin seleccionar nada
    def go_back(self, e):
        from NuevaTransaccion import AddTransactionApp  # Reimporta por si se llama externamente
        self.page.controls.clear()  # Limpia la pantalla
        AddTransactionApp(self.page, self.main_app)  # Vuelve a la pantalla de transacción
