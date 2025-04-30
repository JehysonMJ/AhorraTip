# Importación de módulos necesarios
import flet as ft  # Flet para crear la interfaz gráfica
import datetime  # Para obtener la fecha actual
import time  # Para simular una pausa después de registrar
from Sesion import usuario_actual
from pymongo import MongoClient
import certifi

def conectar_mongo():
    client = MongoClient("mongodb+srv://jmj252004:3lBz9QwY7Uc0If2T@ahorratip.jvgcrrh.mongodb.net/?retryWrites=true&w=majority",
                         tlsCAFile=certifi.where())
    db = client["AhorraTip"]
    return db

# Clase principal para añadir una transacción
class AddTransactionApp:
    def __init__(self, page: ft.Page):
        self.page = page  # Guarda referencia a la página actual
        self.selected_category = None  # Categoría seleccionada (ninguna al inicio)
        self.transaction_type = "GASTOS"  # Tipo de transacción activa (GASTOS o INGRESOS)
        self.build()  # Construye la interfaz

    # Método que construye toda la interfaz de la pantalla
    def build(self):
        # Campo de texto para ingresar el monto
        self.amount_field = ft.TextField(
            hint_text="0",  # Texto guía
            text_align=ft.TextAlign.CENTER,
            width=200,
            height=60,
            text_style=ft.TextStyle(size=28, weight="bold"),  # Estilo grande y negrita
            suffix_text="MXN"  # Moneda al final
        )

        # Fila de pestañas para cambiar entre GASTOS e INGRESOS
        tabs = ft.Row([
            ft.Container(
                content=ft.TextButton(
                    "GASTOS",
                    on_click=lambda e: self.change_tab("GASTOS"),
                    style=ft.ButtonStyle(
                        shape=ft.RoundedRectangleBorder(radius=25),
                        side=ft.BorderSide(2, "white") if self.transaction_type == "GASTOS" else None,
                        color="white" if self.transaction_type == "GASTOS" else "#888888",
                        bgcolor="transparent",
                        padding=ft.Padding(20, 10, 20, 10),
                    ),
                ),
                expand=1,
                alignment=ft.alignment.center_left,
            ),
            ft.Container(
                content=ft.TextButton(
                    "INGRESOS",
                    on_click=lambda e: self.change_tab("INGRESOS"),
                    style=ft.ButtonStyle(
                        shape=ft.RoundedRectangleBorder(radius=25),
                        side=ft.BorderSide(2, "white") if self.transaction_type == "INGRESOS" else None,
                        color="white" if self.transaction_type == "INGRESOS" else "#888888",
                        bgcolor="transparent",
                        padding=ft.Padding(20, 10, 20, 10),
                    ),
                ),
                expand=1,
                alignment=ft.alignment.center_right,
            )
        ])

        # Sección de categorías
        categories = self.build_categories()

        # Texto con la fecha actual
        today = datetime.date.today().strftime("%d/%m")
        self.date_text = ft.Text(f"Hoy ({today})", size=14)

        # Campo para ingresar un comentario
        self.comment_field = ft.TextField(
            label="Comentario",
            multiline=True,
            min_lines=2,
            max_lines=4,
            width=300
        )

        # Botón para añadir la transacción
        add_button = ft.ElevatedButton(
            text="Añadir",
            bgcolor="#FFEB3B",
            color="#000000",
            width=220,
            height=45,
            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=25)),
            on_click=self.add_transaction
        )

        # Botón para regresar a la pantalla anterior
        back_button = ft.TextButton("← Volver", on_click=self.go_back)

        # Agrega todos los componentes a la página
        self.page.controls.clear()
        self.page.floating_action_button = None  # Oculta el botón flotante
        self.page.add(
            ft.Column([
                ft.Text("Añadir Transacción", size=28, weight="bold"),  # Título
                tabs,  # Pestañas
                self.amount_field,  # Monto
                ft.Text("Categorías:", size=16, weight="bold"),  # Etiqueta
                categories,  # Categorías dinámicas
                self.date_text,  # Fecha
                self.comment_field,  # Comentario
                add_button,  # Botón para guardar
                back_button  # Botón para volver
            ],
                alignment=ft.MainAxisAlignment.START,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=20,
                scroll=ft.ScrollMode.AUTO  # Activa scroll automático
            )
        )
        self.page.update()

    def go_back(self, e):
        from MainApp import MainApp
        self.page.controls.clear()
        MainApp(self.page)
        
    # Método que construye las categorías según el tipo de transacción
    def build_categories(self):
        if self.transaction_type == "GASTOS":
            return ft.Column([
                ft.Row([
                    self.category_chip("❤️", "Salud", "#e53935"),
                    self.category_chip("💳", "Ocio", "#43a047"),
                    self.category_chip("🏠", "Casa", "#1e88e5"),
                    self.category_chip("☕", "Café", "#fdd835"),
                ], alignment=ft.MainAxisAlignment.CENTER, spacing=20),
                ft.Row([
                    self.category_chip("🎓", "Educación", "#ab47bc"),
                    self.category_chip("🎁", "Regalos", "#aed581"),
                    self.category_chip("🛒", "Alimentación", "#4fc3f7"),
                    self.category_chip("➕", "Más", "#90a4ae"),
                ], alignment=ft.MainAxisAlignment.CENTER, spacing=20),
            ], spacing=20)
        else:
            return ft.Column([
                ft.Row([
                    self.category_chip("🪙", "Salario", "#1e88e5"),
                    self.category_chip("🎁", "Regalo", "#ec407a"),
                    self.category_chip("🏦", "Interés", "#66bb6a"),
                    self.category_chip("❓", "Otros", "#81c784"),
                ], alignment=ft.MainAxisAlignment.CENTER, spacing=20),
                ft.Row([
                    self.category_chip("💵", "Beca", "#fdd835"),
                    self.category_chip("🤝", "Pago", "#4dd0e1"),
                    self.category_chip("🎫", "Aguinaldo", "#f06292"),
                ], alignment=ft.MainAxisAlignment.CENTER, spacing=20),
            ], spacing=20)

    # Método que crea cada categoría con ícono y color
    def category_chip(self, emoji, name, color):
        selected = (self.selected_category == name)  # Verifica si está seleccionada
        return ft.GestureDetector(
            on_tap=lambda e: self.select_category(name),  # Al hacer clic, se selecciona
            content=ft.Container(
                content=ft.Column([
                    ft.Container(
                        content=ft.Text(emoji, size=22),  # Ícono de la categoría
                        width=60,
                        height=60,
                        bgcolor=color if not selected else "#000000",  # Si está seleccionada, se oscurece
                        border_radius=30,
                        alignment=ft.alignment.center
                    ),
                    ft.Text(name, size=12, text_align="center", color="#FFFFFF" if selected else "#CCCCCC")
                ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                padding=5,
                width=70
            )
        )

    # Método para seleccionar categoría o redirigir si se elige "Más"
    def select_category(self, name):
        if name == "Más":
            from NuevaCategoria import NuevaCategoria  # Redirige a crear nueva categoría
            self.page.controls.clear()
            NuevaCategoria(self.page)
            return

        # Guarda el valor actual y reconstruye manteniéndolo
        current_amount = self.amount_field.value
        current_comment = self.comment_field.value
        self.selected_category = name
        self.build()
        self.amount_field.value = current_amount
        self.comment_field.value = current_comment
        self.page.update()

    # Cambia el tipo de transacción (GASTOS o INGRESOS)
    def change_tab(self, tab_name):
        self.transaction_type = tab_name
        self.build()  # Reconstruye todo con la nueva pestaña activa

    # Método para validar y registrar la transacción
    def add_transaction(self, e):
        monto = self.amount_field.value.strip()
        comentario = self.comment_field.value.strip()

        if not monto or not monto.replace(".", "", 1).isdigit() or float(monto) <= 0:
            self.page.snack_bar = ft.SnackBar(content=ft.Text("Ingresa un monto válido."), bgcolor="red")
            self.page.snack_bar.open = True
            self.page.update()
            return

        if not self.selected_category:
            self.page.snack_bar = ft.SnackBar(content=ft.Text("Selecciona una categoría."), bgcolor="red")
            self.page.snack_bar.open = True
            self.page.update()
            return

        # 🟢 Crear documento para guardar en MongoDB
        from datetime import datetime
        from LoginApp import conectar_mongo

        db = conectar_mongo()
        gastos_col = db["gastos"]

        gasto = {
            "usuario": usuario_actual.strip(),  # Aquí podrías usar el usuario activo
            "categoria": self.selected_category,
            "emoji": "",  # Si manejas emoji, puedes añadirlo
            "color": "",  # Lo mismo con color
            "monto": float(monto),
            "comentario": comentario,
            "fecha": datetime.now(),
            "tipo": self.transaction_type
        }

        gastos_col.insert_one(gasto)

        self.page.snack_bar = ft.SnackBar(content=ft.Text("Transacción añadida correctamente ✅"), bgcolor="#c6ff00")
        self.page.snack_bar.open = True
        self.page.update()
        time.sleep(1)

        from MainApp import MainApp
        self.page.controls.clear()
        main_app = MainApp(self.page)
        main_app.actualizar_grafico()
