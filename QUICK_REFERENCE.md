# ⚡ Guía Rápida - Comandos Esenciales

## 🚀 Instalación (Primera Vez)

### Mac/Linux:
```bash
./install.sh
```

### Windows:
```cmd
install.bat
```

---

## 🎮 Comandos Diarios

### Ver estado del contenedor:
```bash
docker ps
```

### Ver logs en tiempo real:
```bash
docker logs -f n8n-lead-generator
```

### Reiniciar:
```bash
docker-compose restart
```

### Detener:
```bash
docker-compose down
```

### Iniciar:
```bash
docker-compose up -d
```

---

## 🔧 Mantenimiento

### Actualizar después de cambios en código:
```bash
docker-compose down
docker-compose build --no-cache
docker-compose up -d
```

### Ver logs de errores:
```bash
docker logs n8n-lead-generator | grep -i error
```

### Limpiar todo y empezar de cero:
```bash
docker-compose down -v
docker-compose build --no-cache
docker-compose up -d
```

---

## 🐛 Debug

### Acceder al contenedor:
```bash
docker exec -it n8n-lead-generator /bin/sh
```

### Dentro del contenedor:
```bash
# Ver scripts
ls -la /data/scripts/

# Probar Python
python3 --version

# Ver variables de entorno
env | grep GOOGLE

# Ejecutar pipeline manualmente
cd /data/scripts
bash run_pipeline.sh "test query" 5
```

### Ver archivos generados:
```bash
# En el host
ls -la output/

# Dentro del contenedor
ls -la /data/scripts/.tmp/
```

---

## 📊 N8N

### Acceso:
```
http://localhost:5678
Usuario: admin
Contraseña: (ver docker-compose.yml)
```

### Importar workflow:
1. Workflows → Import from File
2. Seleccionar: `workflows/n8n_pipeline_workflow.json`

### Ejecutar manualmente:
1. Abrir workflow
2. Editar "Set Variables"
3. Click "Execute Workflow"

### Activar ejecución automática:
1. Toggle en esquina superior derecha
2. Verificar que "Schedule Trigger" está activo

---

## 🔑 Configuración

### Editar variables de entorno:
```bash
nano .env  # o notepad .env en Windows
```

### Cambiar contraseña de N8N:
```bash
nano docker-compose.yml
# Buscar: N8N_BASIC_AUTH_PASSWORD
# Cambiar valor
docker-compose restart
```

### Cambiar puerto de N8N:
```bash
nano docker-compose.yml
# Buscar: ports: - "5678:5678"
# Cambiar a: - "8080:5678"
docker-compose restart
```

---

## 📂 Ubicaciones Importantes

### En el host:
```
.env                    → Credenciales
output/                 → CSVs generados
workflows/              → Workflows N8N
directives/             → Documentación
```

### Dentro del contenedor:
```
/data/scripts/          → Scripts Python
/data/scripts/.env      → Credenciales (montado)
/data/scripts/.tmp/     → CSVs temporales
/home/node/.n8n/        → Datos N8N
```

---

## 🌐 Acceso Remoto

### Cloudflare Tunnel (Recomendado):
```bash
cloudflared tunnel --url http://localhost:5678
```

### Ngrok (Temporal):
```bash
ngrok http 5678
```

### Desde otra máquina en tu red:
```
http://<ip-servidor>:5678
```

---

## ✅ Checklist de Verificación

Antes de usar en producción:

- [ ] `.env` configurado con API keys reales
- [ ] Contraseña de N8N cambiada
- [ ] Workflow importado
- [ ] Ejecución manual funciona
- [ ] CSV se genera en `output/`
- [ ] Google Sheets conectado (si aplica)
- [ ] Schedule trigger activado
- [ ] Logs sin errores

---

## 🆘 Problemas Comunes

### "Cannot connect to Docker daemon"
→ Inicia Docker Desktop

### "Port already in use"
→ Cambia puerto en `docker-compose.yml`

### "Permission denied"
→ En Linux: `sudo usermod -aG docker $USER`

### "Module not found"
→ `docker-compose build --no-cache`

### No se genera CSV
→ Verifica `.env` y revisa logs

---

## 📞 Comandos de Soporte

### Información del sistema:
```bash
docker --version
docker-compose --version
docker info
```

### Espacio en disco:
```bash
docker system df
```

### Limpiar recursos no usados:
```bash
docker system prune -a
```

---

## 🎯 Flujo de Trabajo Típico

### Desarrollo (Mac):
```bash
# 1. Hacer cambios en código
nano execution/scrape_gmb_api.py

# 2. Reconstruir
docker-compose build

# 3. Reiniciar
docker-compose restart

# 4. Probar
docker logs -f n8n-lead-generator
```

### Producción (Windows Server):
```bash
# 1. Pull cambios
git pull

# 2. Reconstruir
docker-compose build

# 3. Reiniciar
docker-compose restart

# 4. Verificar
docker ps
```

---

## 📚 Documentación Completa

- [README.md](../README.md) - Documentación principal
- [DOCKER_SETUP.md](DOCKER_SETUP.md) - Guía de instalación
- [RESUMEN_ARQUITECTURA.md](RESUMEN_ARQUITECTURA.md) - Arquitectura completa
- [ARCHITECTURE_DIAGRAMS.md](ARCHITECTURE_DIAGRAMS.md) - Diagramas visuales

---

**💡 Tip:** Guarda este archivo en favoritos para acceso rápido
