import flet as ft

# Credenciales de prueba
USUARIO_VALIDO = "admin"
CONTRASENA_VALIDA = "1234"

def main(page: ft.Page):
    page.title = "Login App"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    # Definir los campos de entrada
    usuario_input = ft.TextField(label="Usuario", width=300)
    contrasena_input = ft.TextField(label="Contraseña", password=True, can_reveal_password=True, width=300)
    mensaje_error = ft.Text(color="red")

    def login_click(e):
        usuario = usuario_input.value
        contrasena = contrasena_input.value

        # Validación simple de credenciales
        if usuario == USUARIO_VALIDO and contrasena == CONTRASENA_VALIDA:
            page.controls.clear()
            page.add(ft.Text(f"¡Bienvenido, {usuario}!", size=24))
        else:
            mensaje_error.value = "Usuario o contraseña incorrectos."
            page.update()

    # Botón de login
    login_button = ft.ElevatedButton(text="Iniciar Sesión", on_click=login_click)

    # Añadir los elementos a la página
    page.add(
        ft.Column(
            [
                ft.Text("Iniciar Sesión", size=30, weight="bold"),
                usuario_input,
                contrasena_input,
                login_button,
                mensaje_error,
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )
    )

ft.app(target=main)
