import flet as ft
import datetime
import time

class AddTransactionApp:
    def __init__(self, page: ft.Page):
        self.page = page
        self.selected_category = None
        self.transaction_type = "GASTOS"
        self.build()

    def build(self):
        self.amount_field = ft.TextField(
            hint_text="0",
            text_align=ft.TextAlign.CENTER,
            width=200,
            height=60,
            text_style=ft.TextStyle(size=28, weight="bold"),
            suffix_text="MXN"
        )

        # Nueva fila de botones simulando tabs centrados
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

        categories = self.build_categories()

        today = datetime.date.today().strftime("%d/%m")
        self.date_text = ft.Text(f"Hoy ({today})", size=14)

        self.comment_field = ft.TextField(
            label="Comentario",
            multiline=True,
            min_lines=2,
            max_lines=4,
            width=300
        )

        add_button = ft.ElevatedButton(
            text="Añadir",
            bgcolor="#FFEB3B",
            color="#000000",
            width=220,
            height=45,
            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=25)),
            on_click=self.add_transaction
        )

        back_button = ft.TextButton("← Volver", on_click=self.go_back)

        self.page.controls.clear()
        self.page.floating_action_button = None
        self.page.add(
            ft.Column([
                ft.Text("Añadir Transacción", size=28, weight="bold"),
                tabs,
                self.amount_field,
                ft.Text("Categorías:", size=16, weight="bold"),
                categories,
                self.date_text,
                self.comment_field,
                add_button,
                back_button
            ],
                alignment=ft.MainAxisAlignment.START,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=20,
                scroll=ft.ScrollMode.AUTO)
        )
        self.page.update()

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
                    self.category_chip("➕", "Más", "#90a4ae"),
                ], alignment=ft.MainAxisAlignment.CENTER, spacing=20),
            ], spacing=20)

    def category_chip(self, emoji, name, color):
        selected = (self.selected_category == name)
        return ft.GestureDetector(
            on_tap=lambda e: self.select_category(name),
            content=ft.Container(
                content=ft.Column([
                    ft.Container(
                        content=ft.Text(emoji, size=22),
                        width=60,
                        height=60,
                        bgcolor=color if not selected else "#000000",
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

    def select_category(self, name):
        current_amount = self.amount_field.value
        current_comment = self.comment_field.value
        self.selected_category = name
        self.build()
        self.amount_field.value = current_amount
        self.comment_field.value = current_comment
        self.page.update()

    def change_tab(self, tab_name):
        self.transaction_type = tab_name
        self.build()

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
        self.page.snack_bar = ft.SnackBar(content=ft.Text("Transacción añadida correctamente ✅"), bgcolor="#c6ff00")
        self.page.snack_bar.open = True
        self.page.update()
        time.sleep(1)
        from MainApp import MainApp
        self.page.controls.clear()
        MainApp(self.page)

    def go_back(self, e):
        from MainApp import MainApp
        self.page.controls.clear()
        MainApp(self.page)
