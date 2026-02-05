# 🚀 Lead Generator - Sistema Automatizado de Generación de Leads

Sistema profesional de generación de leads usando Google Places API, análisis de pain points y automatización con N8N.

## 🎯 Características

- ✅ **Búsqueda automatizada** de negocios vía Google Places API
- ✅ **Análisis de pain points** mediante scraping web
- ✅ **Enriquecimiento de datos** con LinkedIn y redes sociales
- ✅ **Exportación automática** a Google Sheets
- ✅ **Programación flexible** (semanal, diaria, manual)
- ✅ **Todo-en-uno**: N8N + Python en un solo contenedor Docker

---

## 🏗️ Arquitectura

```
┌─────────────────────────────────────────┐
│   Docker Container (Todo-en-Uno)       │
│   ┌─────────────────────────────────┐   │
│   │  N8N (Orquestador)              │   │
│   │  - Schedule Trigger             │   │
│   │  - Manual Execution             │   │
│   └──────────────┬──────────────────┘   │
│                  │                       │
│   ┌──────────────▼──────────────────┐   │
│   │  Python Pipeline                │   │
│   │  1. Search (Google Places)      │   │
│   │  2. Deduplicate                 │   │
│   │  3. Analyze (Pain Points)       │   │
│   │  4. Enrich (LinkedIn/Social)    │   │
│   │  5. Export (CSV)                │   │
│   └─────────────────────────────────┘   │
└─────────────────────────────────────────┘
                  ↓
          Google Sheets
```

**Ventajas de esta arquitectura:**
- 🎯 **Simple**: Un solo contenedor, sin SSH
- 🔄 **Portable**: Funciona igual en Windows, Mac, Linux, Cloud
- 📦 **Replicable**: Fácil de instalar para clientes
- 🛠️ **Mantenible**: Actualizaciones con `docker-compose build`

---

## ⚡ Instalación Rápida

### Opción 1: Script Automático (Recomendado)

**En Windows:**
```bash
install.bat
```

**En Mac/Linux:**
```bash
./install.sh
```

### Opción 2: Manual

```bash
# 1. Configurar variables de entorno
cp .env.template .env
# Edita .env con tus API keys

# 2. Construir y levantar
docker-compose build
docker-compose up -d

# 3. Acceder a N8N
# http://localhost:5678
# Usuario: admin
# Contraseña: (ver docker-compose.yml)
```

---

## 📋 Requisitos Previos

1. **Docker Desktop** instalado y corriendo
   - Windows/Mac: https://www.docker.com/products/docker-desktop
   - Linux: `sudo apt install docker.io docker-compose`

2. **Google APIs configuradas:**
   - Google Places API Key ([Guía](directives/google_places_api_setup.md))
   - Google Custom Search API Key (opcional) ([Guía](directives/google_cse_setup.md))
   - Google Sheets API (opcional, para export automático)

---

## 🎮 Uso

### Ejecución Manual

1. Accede a N8N: `http://localhost:5678`
2. Abre el workflow "Lead Generator - Automated Pipeline"
3. Edita el nodo **"Set Variables"**:
   - `query`: "abogados en Madrid"
   - `limit`: 20
4. Click **"Execute Workflow"**
5. Espera 1-2 minutos
6. Resultados en `output/sheets_import_*.csv` o Google Sheets

### Ejecución Automática

El workflow está configurado para ejecutarse **automáticamente cada lunes a las 9:00 AM**.

Para cambiar la frecuencia:
1. Edita el nodo **"Schedule Trigger"**
2. Ajusta día/hora
3. Guarda el workflow
4. Asegúrate de que el workflow esté **activado** (toggle superior derecho)

---

## 📂 Estructura del Proyecto

```
Buscador-Rate-Leads/
├── 📄 Dockerfile                    # Imagen Docker custom (N8N + Python)
├── 📄 docker-compose.yml            # Orquestación
├── 📄 .env                          # Credenciales (NO subir a Git)
├── 📄 install.sh / install.bat      # Scripts de instalación
│
├── 📁 execution/                    # Scripts Python
│   ├── scrape_gmb_api.py           # Búsqueda Google Places
│   ├── deduplicate_leads.py        # Eliminar duplicados
│   ├── analyze_pain_points.py      # Análisis de pain points
│   ├── enrich_leads.py             # Enriquecimiento LinkedIn
│   ├── export_to_sheets_csv.py     # Exportar a CSV
│   └── requirements.txt            # Dependencias Python
│
├── 📁 workflows/                    # Workflows N8N
│   └── n8n_pipeline_workflow.json  # Workflow principal
│
├── 📁 directives/                   # Documentación técnica
│   ├── DOCKER_SETUP.md             # Guía de instalación Docker
│   ├── google_places_api_setup.md  # Setup Google Places API
│   └── google_cse_setup.md         # Setup Google CSE
│
└── 📁 output/                       # CSVs generados (montado desde host)
```

---

## 🔧 Comandos Útiles

### Ver logs en tiempo real:
```bash
docker logs -f n8n-lead-generator
```

### Reiniciar el contenedor:
```bash
docker-compose restart
```

### Detener el sistema:
```bash
docker-compose down
```

### Actualizar después de cambios en código:
```bash
docker-compose down
docker-compose build --no-cache
docker-compose up -d
```

### Acceder al contenedor (debug):
```bash
docker exec -it n8n-lead-generator /bin/sh
```

---

## 🌐 Acceso Remoto (Opcional)

Si quieres acceder a N8N desde fuera de tu red local:

### Opción 1: Cloudflare Tunnel (Recomendado, gratis)
```bash
cloudflared tunnel --url http://localhost:5678
```

### Opción 2: Ngrok (Temporal)
```bash
ngrok http 5678
```

### Opción 3: Port Forwarding + DuckDNS
1. Configura port forwarding en tu router (puerto 5678)
2. Registra un dominio en https://www.duckdns.org
3. Accede vía: `http://tu-dominio.duckdns.org:5678`

---

## 👥 Para Clientes: Instalación Simplificada

Este sistema está diseñado para ser fácilmente replicable a clientes:

### Instalación en 3 pasos:

1. **Clonar repositorio:**
   ```bash
   git clone <tu-repo> lead-generator
   cd lead-generator
   ```

2. **Configurar credenciales:**
   ```bash
   cp .env.template .env
   # Editar .env con API keys del cliente
   ```

3. **Instalar:**
   ```bash
   ./install.sh  # o install.bat en Windows
   ```

### Migración a Cloud (VPS):

El mismo `docker-compose.yml` funciona en cualquier VPS:

```bash
# En DigitalOcean, Hetzner, AWS, etc.
git clone <tu-repo>
cd lead-generator
cp .env.template .env
# Editar .env
docker-compose up -d

# Acceso remoto con Cloudflare Tunnel
cloudflared tunnel --url http://localhost:5678
```

---

## 🐛 Solución de Problemas

### "Cannot connect to Docker daemon"
- Asegúrate de que Docker Desktop está corriendo

### "Port 5678 already in use"
- Cambia el puerto en `docker-compose.yml`:
  ```yaml
  ports:
    - "8080:5678"
  ```

### No se generan archivos CSV
1. Verifica que `.env` tiene las API keys correctas
2. Revisa logs: `docker logs n8n-lead-generator`
3. Verifica que la carpeta `output/` existe

### "Module not found" en Python
```bash
docker-compose build --no-cache
docker-compose up -d
```

---

## 📊 Resultados

El sistema genera archivos CSV con la siguiente estructura:

| Campo | Descripción |
|-------|-------------|
| `name` | Nombre del negocio |
| `address` | Dirección completa |
| `phone` | Teléfono |
| `website` | Sitio web |
| `rating` | Calificación Google (1-5) |
| `reviews` | Número de reseñas |
| `pain_points` | Pain points detectados |
| `linkedin_url` | Perfil LinkedIn (si se encuentra) |
| `email` | Email (si se encuentra) |

---

## 📚 Documentación Adicional

- [Guía de Instalación Docker](directives/DOCKER_SETUP.md)
- [Setup Google Places API](directives/google_places_api_setup.md)
- [Setup Google Custom Search](directives/google_cse_setup.md)
- [Análisis de Pain Points](PAIN_POINT_ANALYSIS_GUIDE.md)

---

## 🤝 Soporte

Si encuentras problemas:
1. Revisa los logs: `docker logs n8n-lead-generator`
2. Verifica el `.env` tiene las credenciales correctas
3. Consulta [DOCKER_SETUP.md](directives/DOCKER_SETUP.md)

---

## 📄 Licencia

Este proyecto es privado y confidencial.

---

## 🚀 Roadmap

- [ ] Integración con CRM (HubSpot, Pipedrive)
- [ ] Análisis de sentimiento en reseñas
- [ ] Detección automática de email
- [ ] Dashboard de métricas
- [ ] API REST para integración externa

---

**Desarrollado con ❤️ para generación profesional de leads**
