# Guía de Configuración: Google Places API

Este documento detalla cómo configurar Google Places API para habilitar la búsqueda de leads "infalible" y sin bloqueos.

## 1. Crear Proyecto en Google Cloud

1. Ve a [Google Cloud Console](https://console.cloud.google.com/).
2. Haz clic en el selector de proyectos (arriba a la izquierda) y selecciona **"New Project"**.
3. Nombre del proyecto: `Lead-Generator` (o similar).
4. Haz clic en **"Create"**.

## 2. Habilitar la API

1. En el menú lateral, ve a **"APIs & Services"** > **"Library"**.
2. Busca: **"Places API (New)"** (asegúrate de que diga "New").
   - *Nota: Si no aparece "New", busca simplemente "Places API".*
3. Haz clic en el resultado y luego en **"Enable"**.

## 3. Crear Credenciales (API Key)

1. Ve a **"APIs & Services"** > **"Credentials"**.
2. Haz clic en **"+ CREATE CREDENTIALS"** > **"API key"**.
3. Se generará una clave (empieza por `AIza...`). **Cópiala**.

## 4. Configurar Restricciones (Seguridad)

*Es muy recomendable restringir el uso de tu clave.*

1. Haz clic en el nombre de la API key recién creada para editarla.
2. En **"API restrictions"**, selecciona **"Restrict key"**.
3. En el desplegable, busca y marca **"Places API (New)"** (y "Places API" si aparece separada).
4. Haz clic en **"Save"**.

## 5. Configurar el Proyecto Local

1. Abre el archivo `.env` en la carpeta del proyecto.
   - Si no existe, copia `.env.template` a `.env`.
2. Añade o edita la siguiente línea:

```ini
GOOGLE_PLACES_API_KEY=
```

3. Guarda el archivo `.env`.

## 6. Verificación

Ejecuta el script de prueba para verificar que la conexión funciona:

```bash
python3 execution/scrape_gmb_api.py --query "test" --max-results 1
```

---

## Preguntas Frecuentes

**¿Es gratis?**
Google ofrece **$200 de crédito mensual gratuito**.
- Una búsqueda básica cuesta muy poco.
- Para tu volumen de ~500 leads/mes, el costo estimado es **$0** (cubierto totalmente por el crédito gratis).

**¿Necesito tarjeta de crédito?**
Sí, Google Cloud requiere una tarjeta para verificar identidad y activar el crédito gratuito, pero no te cobrarán si te mantienes dentro del límite (que es bastante alto).
