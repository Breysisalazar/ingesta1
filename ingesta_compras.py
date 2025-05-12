import pandas as pd
import pymysql
import boto3
import logging
import os

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
try:
    logging.info("Paso 1: Conectando a la base de datos")
    conn = pymysql.connect(
        host='mysql_c',
        port=3306,
        user='root',
        password='utec',
        database='compras_db'
    )
    logging.info("Conexion exitosa a MySQL")
    query = """
    SELECT p.id_pasajero, p.nombre_completo, p.email, p.fecha_nacimiento, p.telefono, m.tipo,
           c.id_compra, c.fecha, c.asiento, m.fecha_exploracion
    FROM Pasajero p
    JOIN Membresia m ON p.id_pasajero = m.id_pasajero
    JOIN Compra c ON p.id_pasajero = c.id_pasajero
    """
    df = pd.read_sql(query, conn)
    logging.info(f"Consulta ejecutada correctamente. Registros obtenidos: {len(df)}")
# Guardar como CSV
    csv_file = "compras.csv"
    df.to_csv(csv_file, index=False)
    logging.info(f"Archivo CSV guardado como {csv_file}")
# Subir a S3
    s3 = boto3.client('s3')
    s3.upload_file(csv_file, "ingesta-datos", "ingesta01/compras.csv")
    logging.info("Archivo CSV subido exitosamente a S3")
dpx-gwsd-wgn

except Exception as e:
    logging.error("Ocurrio un error durante la ejecución", exc_info=True)
finally:
    if 'conn' in locals() and conn.open:
        conn.close()
        logging.info("Conexion a la base de datos cerrada")