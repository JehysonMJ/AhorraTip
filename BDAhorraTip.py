from pymongo import MongoClient
from datetime import datetime

# Conectar a MongoDB (ajusta la URI si usas MongoDB Atlas o un host diferente)
client = MongoClient('mongodb://localhost:27017/')
db = client['AhorraTip']  # Seleccionar la base de datos AhorraTip

# 1. Colección: Usuarios
usuarios = db['usuarios']
usuario = {
    "nombre": "Juan Pérez",
    "correo": "juan@example.com",
    "contraseña": "hashed_password_123",
    "fecha_registro": datetime(2025, 4, 2, 10, 0, 0)
}
resultado_usuario = usuarios.insert_one(usuario)
id_usuario = resultado_usuario.inserted_id
print(f"Usuario creado con ID: {id_usuario}")

# 2. Colección: Cuentas
cuentas = db['cuentas']
cuenta = {
    "id_usuario": id_usuario,
    "nombre_cuenta": "Cuenta Ahorros BBVA",
    "tipo_cuenta": "Ahorros",
    "saldo_inicial": 1000.50,
    "fecha_creacion": datetime(2025, 4, 2, 10, 0, 0)
}
resultado_cuenta = cuentas.insert_one(cuenta)
id_cuenta = resultado_cuenta.inserted_id
print(f"Cuenta creada con ID: {id_cuenta}")

# 3. Colección: Transacciones
transacciones = db['transacciones']
transaccion = {
    "id_cuenta": id_cuenta,
    "tipo_transaccion": "Gasto",
    "monto": 50.75,
    "fecha": datetime(2025, 4, 2, 12, 0, 0),
    "descripcion": "Compra supermercado",
    "categoria": "Alimentación"
}
resultado_transaccion = transacciones.insert_one(transaccion)
print(f"Transacción creada con ID: {resultado_transaccion.inserted_id}")

# 4. Colección: Categorías
categorias = db['categorias']
categoria = {
    "id_usuario": id_usuario,
    "nombre_categoria": "Alimentación",
    "tipo": "Gasto"
}
resultado_categoria = categorias.insert_one(categoria)
id_categoria = resultado_categoria.inserted_id
print(f"Categoría creada con ID: {id_categoria}")

# 5. Colección: Presupuestos
presupuestos = db['presupuestos']
presupuesto = {
    "id_usuario": id_usuario,
    "id_categoria": id_categoria,
    "monto_maximo": 200.00,
    "periodo": "Mensual",
    "fecha_inicio": datetime(2025, 4, 1, 0, 0, 0),
    "fecha_fin": datetime(2025, 4, 30, 23, 59, 59)
}
resultado_presupuesto = presupuestos.insert_one(presupuesto)
print(f"Presupuesto creado con ID: {resultado_presupuesto.inserted_id}")

# 6. Colección: Predicciones
predicciones = db['predicciones']
prediccion = {
    "id_usuario": id_usuario,
    "tipo_prediccion": "Gasto mensual",
    "monto_predicho": 300.00,
    "fecha_prediccion": datetime(2025, 4, 2, 15, 0, 0),
    "periodo": "Mayo 2025",
    "confianza": 0.85
}
resultado_prediccion = predicciones.insert_one(prediccion)
print(f"Predicción creada con ID: {resultado_prediccion.inserted_id}")

# 7. Colección: Metas de Ahorro
metas_ahorro = db['metas_ahorro']
meta = {
    "id_usuario": id_usuario,
    "nombre_meta": "Viaje a Europa",
    "monto_objetivo": 2000.00,
    "monto_actual": 500.00,
    "fecha_limite": datetime(2025, 12, 31, 23, 59, 59)
}
resultado_meta = metas_ahorro.insert_one(meta)
print(f"Meta de ahorro creada con ID: {resultado_meta.inserted_id}")

# Cerrar la conexión (opcional, pero buena práctica)
client.close()
print("Base de datos AhorraTip creada exitosamente!")