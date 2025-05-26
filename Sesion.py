# sesion.py
usuario_actual = None
saldo_global = 500.0

def set_usuario_actual(nombre):
    global usuario_actual
    usuario_actual = nombre