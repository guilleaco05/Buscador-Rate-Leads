# Dockerfile - N8N con Python Integrado
FROM n8nio/n8n:latest

# Cambiar a root para instalar dependencias
USER root

# Instalar Python 3, pip, bash y git
RUN apk add --update --no-cache \
    python3 \
    py3-pip \
    bash \
    git \
    curl

# Crear directorio para scripts
RUN mkdir -p /data/scripts

# Copiar scripts de Python
COPY execution/ /data/scripts/execution/
COPY run_pipeline.sh /data/scripts/
COPY .env.template /data/scripts/.env.template

# Hacer ejecutable el script principal
RUN chmod +x /data/scripts/run_pipeline.sh

# Instalar dependencias de Python
COPY execution/requirements.txt /data/scripts/execution/requirements.txt
RUN pip3 install --no-cache-dir -r /data/scripts/execution/requirements.txt

# Crear directorio temporal
RUN mkdir -p /data/scripts/.tmp

# Ajustar permisos para el usuario node (usuario de N8N)
RUN chown -R node:node /data/scripts

# Volver al usuario node
USER node

# Variables de entorno
ENV PYTHONUNBUFFERED=1
ENV PATH="/data/scripts:${PATH}"

# Exponer puerto de N8N
EXPOSE 5678

# Comando por defecto (heredado de la imagen base)
