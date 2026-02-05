# 🎯 Análisis de Puntos de Dolor - Guía Rápida

## ✨ Nueva Funcionalidad para tu Agencia Web

Este sistema analiza automáticamente los sitios web de tus leads para identificar:
- ✅ **Puntos de dolor** (Diseño Web, Automatización, o Ambos)
- ✅ **Detalles específicos** de los problemas encontrados
- ✅ **Puntuación de oportunidad** (1-10)
- ✅ **Nombre del propietario** del negocio
- ✅ **Email del propietario** para contacto directo
- ✅ **Cargo del propietario** (Owner, CEO, Founder, etc.)

---

## 🚀 Uso Rápido (2 Pasos)

### **Paso 1: Generar Leads**
```bash
# Opción A: Scraping real
python3 execution/scrape_gmb_enhanced.py \
  --query "restaurantes en Madrid" \
  --max-results 10 \
  --format json

# Opción B: Demo data
python3 execution/demo_lead_generator.py \
  --query "restaurantes en Madrid" \
  --max-results 10 \
  --format json
```

### **Paso 2: Analizar Puntos de Dolor**
```bash
python3 execution/analyze_pain_points.py \
  --input .tmp/gmb_leads_enhanced_*.json \
  --output-format csv
```

**Resultado**: Archivo CSV con análisis completo listo para importar a Google Sheets!

---

## 📊 Qué Analiza el Sistema

### **1. Problemas de Diseño Web**

El sistema detecta:
- ❌ **No responsive** - Sitio no se adapta a móviles
- ❌ **Carga lenta** - Más de 3 segundos
- ❌ **Sin HTTPS** - Sitio inseguro
- ❌ **Diseño anticuado** - Tecnologías obsoletas (Flash, frames)
- ❌ **Mal SEO** - Sin meta tags, mala estructura
- ❌ **Imágenes sin optimizar** - Sin alt text

**Ejemplo de salida**:
```
Punto de Dolor: Diseño Web
Detalles: No responsive, carga lenta (4.2s), sin HTTPS
Puntuación: 8/10
```

### **2. Oportunidades de Automatización**

El sistema detecta:
- ❌ **Sin chatbot** - No hay asistente virtual
- ❌ **Formularios básicos** - Sin validación automática
- ❌ **Sin sistema de reservas** - Reservas manuales por teléfono
- ❌ **Sin CRM** - No hay integración visible
- ❌ **Sin email marketing** - No hay newsletter
- ❌ **Sin integración social** - Redes sociales no conectadas

**Ejemplo de salida**:
```
Punto de Dolor: Automatización
Detalles: Sin chatbot, formularios básicos, sin sistema de reservas
Puntuación: 6/10
```

### **3. Ambos (Diseño + Automatización)**

Cuando el sitio tiene problemas en ambas áreas:
```
Punto de Dolor: Ambos
Detalles: 4 problemas de diseño, 5 oportunidades de automatización
Puntuación: 9/10
```

### **4. Extracción de Propietario**

El sistema busca en:
- Página "Sobre Nosotros" / "About"
- Sección "Equipo" / "Team"
- Footer del sitio
- Metadata y redes sociales

**Ejemplo de salida**:
```
Nombre Propietario: Juan García
Email Propietario: juan@restaurante.com
Cargo Propietario: Owner
```

---

## 📈 Puntuación de Oportunidad (1-10)

| Score | Significado | Acción Recomendada |
|-------|-------------|-------------------|
| **9-10** | 🔥 Oportunidad excelente | Contactar INMEDIATAMENTE |
| **7-8** | ✅ Buena oportunidad | Alta prioridad |
| **5-6** | ⚠️ Oportunidad moderada | Seguimiento estándar |
| **3-4** | 📧 Baja prioridad | Outreach masivo |
| **1-2** | ❌ No es buen prospecto | Skip |

---

## 🎯 Workflow Completo

### **1. Generar Leads con Scraping**
```bash
python3 execution/scrape_gmb_enhanced.py \
  --query "tu nicho en tu ciudad" \
  --max-results 20 \
  --format json
```

### **2. Analizar Puntos de Dolor**
```bash
python3 execution/analyze_pain_points.py \
  --input .tmp/gmb_leads_enhanced_*.json \
  --output-format csv
```

### **3. Exportar a Google Sheets**
```bash
python3 execution/export_to_sheets.py \
  --input .tmp/leads_analyzed_*.csv \
  --sheet-name "Leads Analizados - [Tu Ciudad]"
```

### **4. Abrir Google Sheet y Filtrar**
- Abre el link que te da el script
- Filtra por "Puntuación Oportunidad" >= 7
- Ordena por puntuación (mayor a menor)
- ¡Empieza tu outreach con los mejores leads!

---

## 📊 Ejemplo de Salida CSV

```csv
Lead #,Business Name,Website,Punto de Dolor,Detalles del Punto de Dolor,Puntuación Oportunidad,Nombre Propietario,Email Propietario,Cargo Propietario
1,Restaurante La Esquina,https://laesquina.com,Ambos,"No responsive, sin chatbot, formularios básicos",9,María López,maria@laesquina.com,Owner
2,Café Central,https://cafecentral.es,Diseño Web,"Carga lenta (5.1s), diseño anticuado",7,N/A,info@cafecentral.es,N/A
3,Pizzería Roma,https://pizzeriaroma.com,Automatización,"Sin reservas online, sin email marketing",6,Carlos Ruiz,carlos@pizzeriaroma.com,CEO
```

---

## 💡 Estrategia de Outreach

### **Para Leads con "Diseño Web"**

**Email Template**:
```
Asunto: Tu sitio web está perdiendo clientes - [Business Name]

Hola [Nombre Propietario],

Encontré [Business Name] en Google y noté que tu sitio web 
[detalles del punto de dolor].

Esto significa que estás perdiendo clientes que buscan desde móviles 
(más del 70% del tráfico hoy en día).

En [Tu Agencia], ayudamos a negocios como el tuyo a:
✓ Diseño responsive que convierte visitas en clientes
✓ Velocidad de carga 3x más rápida
✓ SEO optimizado para aparecer primero en Google

¿Te interesa una auditoría gratuita de 15 minutos?

Saludos,
[Tu Nombre]
```

### **Para Leads con "Automatización"**

**Email Template**:
```
Asunto: Automatiza y ahorra 10 horas/semana - [Business Name]

Hola [Nombre Propietario],

Vi que [Business Name] gestiona [detalles del punto de dolor] manualmente.

Imagina poder:
✓ Recibir reservas 24/7 sin contestar el teléfono
✓ Seguimiento automático de clientes
✓ Emails de marketing que se envían solos

Esto te ahorraría al menos 10 horas por semana.

¿Hablamos 15 minutos esta semana?

Saludos,
[Tu Nombre]
```

### **Para Leads con "Ambos"**

**Email Template**:
```
Asunto: Multiplica tus ventas online - [Business Name]

Hola [Nombre Propietario],

Analicé [Business Name] y encontré [puntuación] oportunidades 
de mejora que están limitando tus ventas online.

Los problemas principales:
• [Detalle 1]
• [Detalle 2]
• [Detalle 3]

La buena noticia: son fáciles de solucionar y el ROI es inmediato.

¿Te preparo una propuesta personalizada sin compromiso?

Saludos,
[Tu Nombre]
```

---

## 🎨 Google Sheets con Nuevas Columnas

Cuando exportes a Google Sheets, verás:

| Lead # | Business Name | ... | **Punto de Dolor** | **Detalles** | **Puntuación** | **Propietario** | **Email** | **Cargo** |
|--------|---------------|-----|-------------------|--------------|----------------|-----------------|-----------|-----------|
| 1 | Restaurant A | ... | Ambos | No responsive, sin chatbot | 9 | Juan García | juan@... | Owner |
| 2 | Café B | ... | Diseño Web | Carga lenta, mal SEO | 7 | N/A | info@... | N/A |
| 3 | Pizzería C | ... | Automatización | Sin reservas online | 6 | María López | maria@... | CEO |

**Columnas resaltadas**:
- Puntuación 9-10: Verde oscuro
- Puntuación 7-8: Verde claro
- Puntuación 5-6: Amarillo

---

## ⚡ Comandos Rápidos

### **Análisis Rápido (Demo Data)**
```bash
# 1. Generar demo data
python3 execution/demo_lead_generator.py \
  --query "restaurantes en Madrid" \
  --max-results 10 \
  --format json

# 2. Analizar (esto toma ~2-3 min para 10 leads)
python3 execution/analyze_pain_points.py \
  --input .tmp/demo_leads_*.json

# 3. Ver resultados
open .tmp/leads_analyzed_*.csv
```

### **Análisis Completo (Real Data)**
```bash
# 1. Scrape real leads
python3 execution/scrape_gmb_enhanced.py \
  --query "tu nicho en tu ciudad" \
  --max-results 20 \
  --format json

# 2. Analizar puntos de dolor
python3 execution/analyze_pain_points.py \
  --input .tmp/gmb_leads_enhanced_*.json

# 3. Exportar a Google Sheets
python3 execution/export_to_sheets.py \
  --input .tmp/leads_analyzed_*.csv \
  --sheet-name "Leads - [Ciudad]"
```

---

## 📊 Resumen del Análisis

Después de analizar, verás un resumen como este:

```
================================================================================
RESUMEN DEL ANÁLISIS
================================================================================

Distribución de Puntos de Dolor:
  Ambos: 5 leads (50%)
  Diseño Web: 3 leads (30%)
  Automatización: 2 leads (20%)

Top 5 Oportunidades (por score):
  1. Restaurante La Esquina - Score: 9/10
     Punto de dolor: Ambos
     Contacto: María López (maria@laesquina.com)
  
  2. Café Central - Score: 8/10
     Punto de dolor: Diseño Web
     Contacto: N/A
  
  3. Pizzería Roma - Score: 7/10
     Punto de dolor: Automatización
     Contacto: Carlos Ruiz (carlos@pizzeriaroma.com)

✓ Análisis completado: 10 leads procesados
✓ Archivo guardado: .tmp/leads_analyzed_20260128_175000.csv
================================================================================
```

---

## ⚠️ Notas Importantes

### **Tiempo de Procesamiento**
- **Por lead**: ~15-30 segundos
- **10 leads**: ~3-5 minutos
- **50 leads**: ~15-25 minutos

### **Tasa de Éxito**
- **Análisis de diseño**: ~95% (casi siempre funciona)
- **Análisis de automatización**: ~90%
- **Extracción de propietario**: ~40-50% (depende del sitio)
- **Extracción de email propietario**: ~30-40%

### **Sitios que No Se Pueden Analizar**
- Sitios caídos o sin acceso
- Sitios que requieren login
- Sitios con CAPTCHA fuerte
- Sitios que bloquean bots

Estos se marcarán como "Sin acceso" automáticamente.

---

## 🎯 Próximos Pasos

1. **Prueba con demo data** para ver cómo funciona
2. **Analiza 10-20 leads reales** de tu nicho
3. **Exporta a Google Sheets** y filtra por puntuación
4. **Contacta a los top 5** con emails personalizados
5. **Mide tu tasa de respuesta** y ajusta tu estrategia

---

## 📚 Archivos Relacionados

- **Directiva**: `directives/analyze_pain_points.md`
- **Script de Análisis**: `execution/analyze_pain_points.py`
- **Script de Export**: `execution/export_to_sheets.py` (actualizado)
- **Guía de Google Sheets**: `GOOGLE_SHEETS_SETUP.md`

---

**¡Tu sistema de generación de leads ahora es mucho más potente!** 🚀

Ahora no solo obtienes contactos, sino que también sabes:
- ✅ Qué problemas tienen
- ✅ Qué servicios necesitan (diseño, automatización, o ambos)
- ✅ Quién es el decisor
- ✅ Cómo contactarlo directamente

**¡Perfecto para outreach personalizado y alta conversión!** 💰
