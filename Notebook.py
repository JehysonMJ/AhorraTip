from pymongo import MongoClient
import certifi
import pandas as pd
import matplotlib.pyplot as plt

# Conexión a MongoDB
def conectar_mongo():
    client = MongoClient("mongodb+srv://jmj252004:3lBz9QwY7Uc0If2T@ahorratip.jvgcrrh.mongodb.net/?retryWrites=true&w=majority",
                         tlsCAFile=certifi.where())
    db = client["AhorraTip"]
    return db["gastos"]

# Usuario actual
usuario_actual = "JehysonMJ"

# Obtener colección
coleccion = conectar_mongo()

# Buscar documentos del usuario actual
datos = list(coleccion.find({"usuario": usuario_actual}))

# Convertir a DataFrame
df = pd.DataFrame(datos)

# Mostrar el DataFrame
if df.empty:
    print("No hay transacciones registradas para este usuario.")
else:
    print(df)

# Agrupar por categoría y sumar los montos
df_categoria = df.groupby("categoria")["monto"].sum()

# Crear gráfica circular
plt.figure(figsize=(6, 6))
plt.pie(df_categoria, labels=df_categoria.index, autopct="%1.1f%%", startangle=90)
plt.title(f"Gastos por Categoría - {usuario_actual}")
plt.axis("equal")  # Para que sea perfectamente circu
plt.show()
