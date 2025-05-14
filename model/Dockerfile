# Usar una imagen base de Python oficial
FROM python:3.11-slim

# Establecer directorio de trabajo en /app
WORKDIR /app

# Copiar requirements.txt para instalar dependencias
COPY requirements.txt .

# Instalar dependencias
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install fastapi uvicorn

# Copiar el resto del código
COPY . .

# Exponer puerto
EXPOSE 5000

# Configurar PYTHONPATH para encontrar los módulos
ENV PYTHONPATH=/app

# Comando para ejecutar la aplicación (cambiado a uvicorn directamente)
CMD ["uvicorn", "app.app:app", "--host", "0.0.0.0", "--port", "5000", "--reload"]