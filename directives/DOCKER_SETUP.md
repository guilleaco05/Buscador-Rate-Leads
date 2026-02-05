# Guía de Instalación - N8N Lead Generator (Docker Integrado)

## 🎯 Arquitectura

Esta solución combina N8N y Python en un **solo contenedor Docker**, eliminando la necesidad de SSH y simplificando el despliegue.

**Ventajas:**
- ✅ Un solo comando para levantar todo
- ✅ Funciona igual en Windows, Mac, Linux, Cloud
- ✅ Fácil de replicar a clientes
- ✅ Sin configuración SSH compleja

---

## 📋 Requisitos Previos

### En tu Servidor Windows:
1. **Docker Desktop** instalado y corriendo
   - Descarga: https://www.docker.com/products/docker-desktop
   - Asegúrate de que WSL2 esté habilitado

2. **Git** (opcional, para clonar el repo)
   - Descarga: https://git-scm.com/download/win

3. **APIs de Google configuradas:**
   - Google Places API Key
   - Google Custom Search API Key (opcional)
   - Google Sheets API credentials (si usas export directo)

---

## 🚀 Instalación Paso a Paso

### Paso 1: Preparar el Proyecto en el Servidor

**Opción A - Clonar desde Git (recomendado):**
```bash
# En PowerShell o Git Bash en Windows
cd C:\Users\TuUsuario\
git clone <tu-repositorio> Buscador-Rate-Leads
cd Buscador-Rate-Leads
```

**Opción B - Copiar manualmente:**
- Copia toda la carpeta del proyecto desde tu Mac al servidor Windows
- Ubicación sugerida: `C:\Users\TuUsuario\Buscador-Rate-Leads`

---

### Paso 2: Configurar Variables de Entorno

1. Copia el archivo de plantilla:
```bash
copy .env.template .env
```

2. Edita el archivo `.env` con tus credenciales:
```bash
notepad .env
```

3. Añade tus API keys:
```env
GOOGLE_PLACES_API_KEY=tu_api_key_aqui
GOOGLE_CSE_API_KEY=tu_cse_key_aqui
GOOGLE_CSE_ID=tu_cse_id_aqui
```

---

### Paso 3: Configurar Docker Compose

Edita `docker-compose.yml` y cambia la contraseña de N8N:

```yaml
- N8N_BASIC_AUTH_PASSWORD=TuContraseñaSegura123
```

---

### Paso 4: Construir y Levantar el Contenedor

```bash
# Construir la imagen Docker (primera vez o después de cambios)
docker-compose build

# Levantar el contenedor
docker-compose up -d

# Verificar que está corriendo
docker ps
```

**Salida esperada:**
```
CONTAINER ID   IMAGE                    STATUS         PORTS
abc123def456   n8n-lead-generator       Up 10 seconds  0.0.0.0:5678->5678/tcp
```

---

### Paso 5: Acceder a N8N

1. Abre tu navegador
2. Ve a: `http://localhost:5678`
3. Login:
   - **Usuario:** `admin`
   - **Contraseña:** La que configuraste en el Paso 3

---

### Paso 6: Importar el Workflow

1. En N8N, ve a **Workflows** → **Import from File**
2. Selecciona: `workflows/n8n_pipeline_workflow.json`
3. El workflow se importará automáticamente

---

### Paso 7: Configurar Google Sheets (Opcional)

Si quieres subir resultados automáticamente a Google Sheets:

1. En N8N, ve a **Credentials** → **New**
2. Selecciona **Google Sheets OAuth2 API**
3. Sigue el proceso de autenticación
4. En el workflow, actualiza el nodo "Append to Google Sheets":
   - Reemplaza `YOUR_GOOGLE_SHEET_ID_HERE` con tu ID real
   - Selecciona las credenciales que creaste

---

### Paso 8: Probar el Workflow

#### Ejecución Manual:

1. Abre el workflow importado
2. Edita el nodo **"Set Variables"**:
   - `query`: "abogados en Vigo" (o tu búsqueda)
   - `limit`: 10 (para prueba rápida)
3. Click en **"Execute Workflow"**
4. Espera 1-2 minutos
5. Verifica los resultados en la carpeta `output/` o en Google Sheets

#### Ejecución Automática:

1. El nodo **"Schedule Trigger"** está configurado para:
   - **Frecuencia:** Cada lunes a las 9:00 AM
2. Para cambiar la frecuencia:
   - Edita el nodo "Schedule Trigger"
   - Ajusta día/hora según necesites
3. **Activa el workflow** (toggle en la esquina superior derecha)

---

## 📂 Estructura de Archivos

```
Buscador-Rate-Leads/
├── Dockerfile                 # Imagen Docker custom
├── docker-compose.yml         # Orquestación
├── .env                       # Credenciales (NO subir a Git)
├── execution/                 # Scripts Python
│   ├── scrape_gmb_api.py
│   ├── analyze_pain_points.py
│   ├── export_to_sheets_csv.py
│   └── requirements.txt
├── workflows/
│   └── n8n_pipeline_workflow.json
├── output/                    # CSVs generados (montado desde host)
└── directives/                # Documentación
```

---

## 🔧 Comandos Útiles

### Ver logs del contenedor:
```bash
docker logs n8n-lead-generator

# Seguir logs en tiempo real
docker logs -f n8n-lead-generator
```

### Reiniciar el contenedor:
```bash
docker-compose restart
```

### Detener el contenedor:
```bash
docker-compose down
```

### Reconstruir después de cambios en código:
```bash
docker-compose down
docker-compose build --no-cache
docker-compose up -d
```

### Acceder al contenedor (debug):
```bash
docker exec -it n8n-lead-generator /bin/sh

# Dentro del contenedor:
cd /data/scripts
ls -la
python3 --version
```

---

## 🌐 Acceso Remoto (Opcional)

Si quieres acceder a N8N desde fuera de tu red local:

### Opción 1: Túnel con Ngrok (Gratis, temporal)
```bash
# Instalar ngrok
# Descargar de: https://ngrok.com/download

# Crear túnel
ngrok http 5678
```

### Opción 2: DuckDNS + Port Forwarding (Gratis, permanente)
1. Registra un dominio en https://www.duckdns.org
2. Configura port forwarding en tu router (puerto 5678)
3. Accede vía: `http://tu-dominio.duckdns.org:5678`

### Opción 3: Cloudflare Tunnel (Recomendado, gratis)
```bash
# Instalar cloudflared
# Seguir guía: https://developers.cloudflare.com/cloudflare-one/connections/connect-apps/

cloudflared tunnel --url http://localhost:5678
```

---

## 🎁 Para Clientes: Instalación Simplificada

Cuando instales esto para un cliente:

1. **Crea un repositorio privado** con el proyecto
2. **Incluye un `.env.template`** con placeholders
3. **Proporciona un script de instalación:**

```bash
# install.sh (para Linux/Mac) o install.bat (para Windows)
#!/bin/bash
echo "🚀 Instalando Lead Generator..."
cp .env.template .env
echo "✏️ Por favor, edita el archivo .env con tus API keys"
read -p "Presiona Enter cuando hayas configurado .env..."
docker-compose build
docker-compose up -d
echo "✅ Instalación completa!"
echo "🌐 Accede a N8N en: http://localhost:5678"
echo "👤 Usuario: admin"
echo "🔑 Contraseña: (la que configuraste en docker-compose.yml)"
```

---

## 🐛 Solución de Problemas

### "Cannot connect to Docker daemon"
- Asegúrate de que Docker Desktop está corriendo
- En Windows, verifica que WSL2 está habilitado

### "Port 5678 already in use"
- Cambia el puerto en `docker-compose.yml`:
  ```yaml
  ports:
    - "8080:5678"  # Ahora accede en localhost:8080
  ```

### "Module not found" en Python
- Reconstruye la imagen:
  ```bash
  docker-compose build --no-cache
  ```

### No se generan archivos CSV
- Verifica que el `.env` tiene las API keys correctas
- Revisa los logs: `docker logs n8n-lead-generator`
- Verifica que la carpeta `output/` existe

---

## ✅ Verificación Final

Antes de dar por terminada la instalación:

- [ ] Docker contenedor corriendo (`docker ps`)
- [ ] N8N accesible en `http://localhost:5678`
- [ ] Workflow importado correctamente
- [ ] Ejecución manual funciona (genera CSV)
- [ ] Google Sheets conectado (si aplica)
- [ ] Schedule trigger activado

---

## 📞 Soporte

Si encuentras problemas:
1. Revisa los logs: `docker logs n8n-lead-generator`
2. Verifica el `.env` tiene las credenciales correctas
3. Asegúrate de que Docker tiene suficiente memoria (mínimo 2GB)

---

## 🚀 Próximos Pasos

Una vez que todo funcione:
1. Personaliza las queries en "Set Variables"
2. Ajusta la frecuencia del Schedule Trigger
3. Configura notificaciones (Email/Telegram)
4. Añade más workflows según necesites
