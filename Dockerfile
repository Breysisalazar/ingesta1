# Usar una imagen base ligera de Python 3
FROM python:3.10-slim
# Establecer el directorio de trabajo dentro del contenedor
WORKDIR /mv_ingesta/microservicio1
# Instalar las dependencias necesarias (boto3 para S3, mysql-connector para MySQL, pandas para manejo de datos)
RUN pip3 install boto3 mysql-connector-python pandas
# Copiar el codigo fuente de la aplicacion al contenedor
COPY . .
# Ejecutar el script de ingesta de datos
CMD ["python", "./ingesta_compras.py"]