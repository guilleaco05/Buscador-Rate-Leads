# Análisis de Puntos de Dolor para Agencia Web

## Objetivo
Analizar sitios web de negocios para identificar oportunidades de mejora (puntos de dolor) y extraer información de contacto de propietarios/directivos para outreach personalizado.

## Inputs
- `input_file`: Archivo de leads con URLs de sitios web (JSON, CSV, TXT)
- `analysis_depth`: Nivel de análisis (basic, standard, deep) - default: standard
- `output_format`: Formato de salida (txt, json, csv) - default: csv

## Ejecución

### Uso Básico
```bash
python execution/analyze_pain_points.py --input .tmp/gmb_leads_enhanced_*.txt
```

### Con Opciones
```bash
python execution/analyze_pain_points.py \
  --input .tmp/gmb_leads_enhanced_*.txt \
  --analysis-depth deep \
  --output-format csv
```

## Outputs

### Nuevos Campos Añadidos

#### 1. **Punto de Dolor** (pain_point)
Categoría principal de oportunidad:
- **"Diseño Web"** - Sitio anticuado, no responsive, mala UX
- **"Automatización"** - Procesos manuales, falta de integración
- **"Ambos"** - Necesita diseño Y automatización
- **"Ninguno"** - Sitio moderno y bien optimizado
- **"Sin Web"** - No tiene sitio web

#### 2. **Detalles del Punto de Dolor** (pain_point_details)
Descripción específica de los problemas encontrados:
- "Sitio no responsive, diseño de 2015"
- "Sin formularios automatizados, sin chatbot"
- "Carga lenta (5.2s), imágenes sin optimizar"
- "Sin integración con redes sociales"

#### 3. **Puntuación de Oportunidad** (opportunity_score)
Escala 1-10 basada en:
- Severidad de problemas técnicos (40%)
- Potencial de mejora en conversión (30%)
- Competitividad del sector (20%)
- Presupuesto estimado del negocio (10%)

#### 4. **Nombre del Propietario** (owner_name)
Extraído de:
- Página "Sobre Nosotros" / "About"
- Sección "Equipo" / "Team"
- Footer del sitio
- Metadata del sitio
- Perfiles de redes sociales vinculados

#### 5. **Email del Propietario** (owner_email)
Extraído de:
- Página de contacto
- Sección "About" / "Team"
- Metadata (si está disponible)
- Patrones comunes: info@, contacto@, nombre@dominio

#### 6. **Cargo del Propietario** (owner_title)
- "Owner", "CEO", "Founder", "Director", "Manager", etc.

## Metodología de Análisis

### 1. Análisis de Diseño Web

#### Indicadores de Problemas:
- **No Responsive**: No se adapta a móviles
- **Diseño Anticuado**: Tecnologías obsoletas (Flash, frames)
- **Velocidad de Carga**: >3 segundos
- **UX Deficiente**: Navegación confusa, CTAs poco claros
- **Accesibilidad**: Falta de contraste, sin alt text
- **SEO**: Sin meta tags, estructura pobre

#### Detección Técnica:
```python
# Viewport meta tag
has_viewport = '<meta name="viewport"' in html

# Frameworks modernos
modern_frameworks = ['React', 'Vue', 'Angular', 'Next.js']

# CSS moderno
has_modern_css = 'flexbox' in css or 'grid' in css

# Velocidad
load_time = measure_page_load()
```

### 2. Análisis de Automatización

#### Indicadores de Oportunidades:
- **Sin Chatbot**: No hay asistente virtual
- **Formularios Básicos**: Sin validación, sin autorespuesta
- **Sin CRM**: No hay integración visible
- **Procesos Manuales**: Reservas por teléfono, sin calendario online
- **Sin Email Marketing**: No hay signup newsletter
- **Sin Integración**: Redes sociales no conectadas

#### Detección Técnica:
```python
# Chatbot
has_chatbot = any(bot in html for bot in ['intercom', 'drift', 'tawk', 'crisp'])

# Formularios
forms = soup.find_all('form')
has_advanced_forms = check_form_automation(forms)

# Integraciones
has_calendar = 'calendly' in html or 'cal.com' in html
has_crm = 'hubspot' in html or 'salesforce' in html
```

### 3. Extracción de Propietario

#### Estrategia de Búsqueda:
1. **Páginas clave**: /about, /team, /nosotros, /equipo
2. **Patrones de nombre**:
   - "Fundador: [Nombre]"
   - "CEO: [Nombre]"
   - "Propietario: [Nombre]"
   - "Owner: [Nombre]"
3. **Metadata**: Schema.org, Open Graph
4. **Redes sociales**: LinkedIn, Facebook business page

#### Extracción de Email:
```python
# Patrones de email de propietario
owner_patterns = [
    r'[a-z]+@' + domain,  # nombre@dominio.com
    r'owner@' + domain,
    r'ceo@' + domain,
    r'founder@' + domain,
    r'director@' + domain
]

# Verificación de cargo
if 'CEO' in context or 'Founder' in context:
    likely_owner_email = True
```

## Puntuación de Oportunidad

### Cálculo (1-10):

```python
score = 0

# Problemas de diseño (0-4 puntos)
if not responsive: score += 2
if load_time > 3: score += 1
if outdated_design: score += 1

# Falta de automatización (0-3 puntos)
if not has_chatbot: score += 1
if not has_crm: score += 1
if manual_processes: score += 1

# Potencial de negocio (0-3 puntos)
if high_reviews: score += 1  # Negocio exitoso
if competitive_sector: score += 1  # Sector competitivo
if has_budget_indicators: score += 1  # Puede pagar

return min(score, 10)
```

### Interpretación:
- **9-10**: Oportunidad excelente - contactar inmediatamente
- **7-8**: Buena oportunidad - alta prioridad
- **5-6**: Oportunidad moderada - seguimiento estándar
- **3-4**: Baja prioridad - outreach masivo
- **1-2**: No es buen prospecto

## Herramientas & Dependencias

### Python Packages
- `selenium` - Navegación web automatizada
- `beautifulsoup4` - Parsing HTML
- `requests` - HTTP requests
- `lxml` - XML/HTML parsing
- `Pillow` - Análisis de imágenes (opcional)

### APIs Opcionales
- **Google PageSpeed API** - Análisis de velocidad
- **Hunter.io API** - Verificación de emails (requiere API key)
- **Clearbit API** - Enriquecimiento de datos (requiere API key)

## Edge Cases & Constraints

### Sitios Sin Acceso
- **Sitio caído**: Marcar como "Sin acceso - verificar manualmente"
- **Requiere login**: Analizar solo página pública
- **Bloqueado por robots.txt**: Respetar y marcar como "Acceso restringido"
- **CAPTCHA**: Marcar para revisión manual

### Información No Disponible
- **Sin página About**: Buscar en footer, redes sociales
- **Sin email visible**: Usar patrones comunes (info@, contacto@)
- **Sin nombre de propietario**: Buscar en redes sociales, Google

### Falsos Positivos
- **Plantillas modernas**: Pueden parecer buenas pero sin personalización
- **Sitios en construcción**: Marcar como "En desarrollo"
- **Sitios de terceros**: Detectar Wix, Squarespace (oportunidad de migración)

## Performance

### Tiempo de Análisis
- **Por lead**: ~15-30 segundos
- **10 leads**: ~3-5 minutos
- **50 leads**: ~15-25 minutos

### Optimizaciones
- Análisis paralelo (max 3 sitios simultáneos)
- Cache de resultados
- Timeout de 10s por página
- Skip de recursos pesados (videos, imágenes grandes)

## Formato de Salida

### CSV Extendido
```csv
lead_number,name,website,pain_point,pain_point_details,opportunity_score,owner_name,owner_email,owner_title,phone,email,facebook,instagram,...
1,Pro Lawn Care,https://prolawncare.com,Diseño Web,"Sitio no responsive, carga lenta (4.2s)",8,John Smith,john@prolawncare.com,Owner,(212) 555-0123,info@prolawncare.com,...
```

### JSON Detallado
```json
{
  "lead_number": 1,
  "business_name": "Pro Lawn Care",
  "website": "https://prolawncare.com",
  "analysis": {
    "pain_point": "Diseño Web",
    "pain_point_details": "Sitio no responsive, carga lenta (4.2s), diseño de 2016",
    "opportunity_score": 8,
    "design_issues": [
      "No responsive",
      "Carga lenta: 4.2s",
      "Sin HTTPS",
      "Imágenes sin optimizar"
    ],
    "automation_gaps": [
      "Sin chatbot",
      "Formulario básico sin validación"
    ]
  },
  "owner_info": {
    "name": "John Smith",
    "email": "john@prolawncare.com",
    "title": "Owner",
    "confidence": "high"
  }
}
```

## Estrategia de Outreach

### Segmentación por Punto de Dolor

#### Diseño Web (Email Template)
```
Asunto: Mejora tu presencia online - [Business Name]

Hola [Owner Name],

Encontré [Business Name] en Google y noté que tu sitio web 
[pain_point_details]. 

En [Tu Agencia], ayudamos a negocios como el tuyo a:
- Diseño responsive que convierte
- Velocidad de carga 3x más rápida
- SEO optimizado para Google

¿Te interesa una auditoría gratuita?
```

#### Automatización (Email Template)
```
Asunto: Automatiza y ahorra 10h/semana - [Business Name]

Hola [Owner Name],

Vi que [Business Name] gestiona [pain_point_details] manualmente.

Podemos automatizar:
- Reservas online 24/7
- Seguimiento automático de clientes
- Integración con tu CRM

¿Hablamos 15 minutos?
```

## Learnings

### Version 1.0 (Inicial)
- Implementación de análisis básico de diseño
- Extracción de emails y nombres
- Puntuación de oportunidad

### Mejoras Futuras
- [ ] Análisis de competencia (comparar con competidores)
- [ ] Screenshot automático del sitio
- [ ] Análisis de contenido (calidad de textos)
- [ ] Detección de tecnologías usadas (WordPress, Shopify, etc.)
- [ ] Estimación de presupuesto del cliente
- [ ] Análisis de tráfico web (si disponible)
- [ ] Integración con CRM para seguimiento
- [ ] Generación automática de propuestas personalizadas
- [ ] A/B testing de mensajes de outreach
