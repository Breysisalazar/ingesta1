import pandas as pd
import pymysql
import boto3

# Conexion a la base de datos MySQL
conn = pymysql.connect(
    host='mysql_c',              # Nombre del contenedor de MySQL
    port=3306,                   # Puerto del contenedor MySQL
    user='root',                 # Usuario de MySQL
    password='utec',             # Contrasena de MySQL
    database='compras_db'        # Nombre de la base de datos
)

# Leer los datos con una consulta SQL
query = """
SELECT p.id_pasajero, p.nombre_completo, p.email, p.fecha_nacimiento, p.telefono, m.tipo,
       c.id_compra, c.fecha, c.asiento, m.fecha_exploracion
FROM Pasajero p
JOIN Membresia m ON p.id_pasajero = m.id_pasajero
JOIN Compra c ON p.id_pasajero = c.id_pasajero
"""
df = pd.read_sql(query, conn)

# Cerrar la conexion
conn.close()

# Guardar los datos como un archivo CSV
csv_file = "compras.csv"
df.to_csv(csv_file, index=False)

# Subir el archivo CSV a S3
s3 = boto3.client('s3')
s3.upload_file(csv_file, "ingesta-datos", "ingesta01/compras.csv")

print("Ingesta completada desde MySQL")
