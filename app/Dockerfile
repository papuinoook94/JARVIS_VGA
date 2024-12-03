FROM python:3.10-slim

# Establecer el directorio de trabajo
WORKDIR /app

# Copiar archivo de dependencias
COPY requirements.txt /app/

# Instalar dependencias
RUN pip install -r requirements.txt

# Copiar el código fuente
COPY . /app/

# Exponer los puertos para backend y frontend
EXPOSE 8000 8501

# Hacer el script ejecutable
RUN chmod +x start.sh

# Comando de inicio
CMD ["/app/start.sh"]
