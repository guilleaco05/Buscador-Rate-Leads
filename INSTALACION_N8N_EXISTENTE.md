# 🎯 Guía de Instalación - Para tu N8N Existente

## Tu Configuración Actual

```
Servidor Windows (Casa)
  └── Docker
      └── N8N (YA INSTALADO ✅)
          └── Cloudflare Tunnel (acceso remoto ✅)

Tu Mac (Trabajo)
  └── Código Python (aquí)
```

---

## ✅ Plan de Acción (Simple y Directo)

### **Paso 1: Copiar Proyecto al Servidor Windows**

#### Opción A: Usando Acceso Remoto (Si tienes RDP/TeamViewer)

1. Conecta a tu servidor Windows
2. Abre el navegador en el servidor
3. Descarga el proyecto desde tu repositorio Git (si lo tienes)
4. O copia manualmente la carpeta `Buscador-Rate-Leads`

#### Opción B: Compartir Carpeta en Red

1. En tu Mac, comparte la carpeta del proyecto
2. Desde el servidor Windows, accede a la carpeta compartida
3. Copia todo a: `C:\Users\TuUsuario\Buscador-Rate-Leads`

#### Opción C: USB/Transferencia Manual

1. Copia la carpeta a una USB
2. Conecta la USB al servidor
3. Copia a: `C:\Users\TuUsuario\Buscador-Rate-Leads`

---

### **Paso 2: Instalar Python en el Servidor Windows**

**En el servidor Windows:**

1. **Descargar Python:**
   - Ve a: https://www.python.org/downloads/
   - Descarga Python 3.10 o superior

2. **Instalar:**
   - Ejecuta el instalador
   - ⚠️ **IMPORTANTE**: Marca "Add Python to PATH"
   - Click "Install Now"

3. **Verificar instalación:**
   ```cmd
   python --version
   pip --version
   ```

4. **Instalar dependencias del proyecto:**
   ```cmd
   cd C:\Users\TuUsuario\Buscador-Rate-Leads
   pip install -r execution\requirements.txt
   ```

---

### **Paso 3: Configurar Variables de Entorno**

**En el servidor Windows:**

```cmd
cd C:\Users\TuUsuario\Buscador-Rate-Leads
copy .env.template .env
notepad .env
```

**Edita el archivo .env:**
```env
GOOGLE_PLACES_API_KEY=tu_api_key_aqui
GOOGLE_CSE_API_KEY=tu_cse_key_aqui
GOOGLE_CSE_ID=tu_cse_id_aqui
```

Guarda y cierra.

---

### **Paso 4: Probar que Funciona**

**En el servidor Windows (CMD o PowerShell):**

```cmd
cd C:\Users\TuUsuario\Buscador-Rate-Leads

python execution\scrape_gmb_api.py --query "abogados en Madrid" --max-results 5 --format json
```

**Resultado esperado:**
- Debería crear un archivo en `.tmp\api_leads_*.json`
- Si ves errores, revisa que el `.env` tiene las API keys correctas

---

### **Paso 5: Importar Workflow en tu N8N Existente**

**Desde tu Mac (o desde donde accedas a N8N):**

1. **Accede a tu N8N** (vía Cloudflare)

2. **Ve a Workflows** → **Import from File**

3. **Selecciona el archivo:**
   - `workflows/n8n_simple_workflow.json`

4. **Edita el workflow importado:**
   - Abre cada nodo que dice "Execute Command"
   - **Actualiza la ruta** `C:\Users\TuUsuario\` con tu ruta real
   - Ejemplo: Si tu usuario es "Guille", cambia a `C:\Users\Guille\`

---

### **Paso 6: Configurar Google Sheets (Opcional)**

Si quieres subir resultados automáticamente a Google Sheets:

1. **En N8N** → **Credentials** → **New**
2. Selecciona **Google Sheets OAuth2 API**
3. Sigue el proceso de autenticación
4. En el workflow, edita el nodo "7. Upload to Google Sheets":
   - Reemplaza `YOUR_GOOGLE_SHEET_ID` con tu ID real
   - Selecciona las credenciales que creaste

---

### **Paso 7: Probar Ejecución Manual**

1. **Abre el workflow** en N8N

2. **Edita el nodo "Set Variables":**
   - `query`: "abogados en Vigo"
   - `limit`: 5 (para prueba rápida)

3. **Click "Execute Workflow"**

4. **Espera 1-2 minutos**

5. **Verifica resultados:**
   - En el servidor Windows: `C:\Users\TuUsuario\Buscador-Rate-Leads\.tmp\`
   - O en Google Sheets (si lo configuraste)

---

### **Paso 8: Activar Ejecución Automática**

1. **En el workflow**, verifica que el nodo "Schedule Trigger" está configurado:
   - Lunes a las 9:00 AM (o lo que prefieras)

2. **Activa el workflow:**
   - Toggle en la esquina superior derecha
   - Debe cambiar a "Active"

3. **Listo!** El workflow se ejecutará automáticamente cada semana

---

## 🔧 Ajustes Importantes

### Actualizar Rutas en el Workflow

En cada nodo "Execute Command", la ruta debe ser la correcta:

**Ejemplo:**
```cmd
cd C:\Users\Guille\Buscador-Rate-Leads && python execution\scrape_gmb_api.py ...
```

**Reemplaza:**
- `C:\Users\Guille\` con tu ruta real
- Usa `&&` para encadenar comandos en Windows

---

## 🐛 Solución de Problemas

### "python: command not found"
→ Python no está en el PATH. Reinstala Python marcando "Add to PATH"

### "No module named 'requests'"
→ Instala dependencias: `pip install -r execution\requirements.txt`

### "Permission denied"
→ Ejecuta CMD como Administrador

### "API key invalid"
→ Verifica que el `.env` tiene las keys correctas

### El workflow falla en N8N
→ Revisa los logs de N8N: Settings → Log Streaming

---

## ✅ Checklist de Verificación

Antes de dar por terminado:

- [ ] Python instalado en servidor Windows
- [ ] Proyecto copiado a `C:\Users\TuUsuario\Buscador-Rate-Leads`
- [ ] Dependencias instaladas (`pip install -r ...`)
- [ ] `.env` configurado con API keys
- [ ] Prueba manual funciona (genera JSON)
- [ ] Workflow importado en N8N
- [ ] Rutas actualizadas en todos los nodos
- [ ] Ejecución manual en N8N funciona
- [ ] CSV se genera correctamente
- [ ] Google Sheets conectado (opcional)
- [ ] Schedule trigger activado

---

## 📊 Arquitectura Final

```
Tu Mac (Desarrollo)
    ↓ (Git/Copia)
Servidor Windows
    ├── Python + Scripts
    └── Docker
        └── N8N (existente)
            ├── Workflow importado
            └── Execute Command → Python Scripts
                ↓
            Google Sheets
```

---

## 🎯 Resumen

**Lo que NO necesitas hacer:**
- ❌ Tumbar tu N8N actual
- ❌ Crear un nuevo contenedor Docker
- ❌ Configurar SSH
- ❌ Instalar nada en tu Mac

**Lo que SÍ necesitas hacer:**
- ✅ Copiar proyecto al servidor Windows
- ✅ Instalar Python en el servidor
- ✅ Importar workflow en tu N8N existente
- ✅ Actualizar rutas en el workflow
- ✅ Listo!

---

## 📞 Siguiente Paso

**Empieza por el Paso 1:** Copia el proyecto al servidor Windows.

Una vez hecho, avísame y te ayudo con el siguiente paso.
