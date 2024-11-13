# Usa la imagen de Python 3.11
FROM python:3.11

# Establece el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copia el archivo de requerimientos a la imagen
COPY requirements.txt .

# Instala las dependencias
RUN pip install -r requirements.txt

# Copia el resto del código de la aplicación a la imagen
COPY . .

# Expone el puerto en el que correrá Flask (3000 en este caso)
EXPOSE 3000

# Define la variable de entorno FLASK_APP
ENV FLASK_APP=App.py

# Define el comando para ejecutar la aplicación
CMD ["flask", "run", "--host=0.0.0.0", "--port=3000"]
