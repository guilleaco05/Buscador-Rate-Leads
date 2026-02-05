# Guía de Configuración: Google Custom Search API + CSE

Para buscar en LinkedIn e InfoCIF de forma automática ("infalible"), necesitamos un motor de búsqueda personalizado.

## Paso 1: Habilitar la API
1. Ve a la [Consola de Google Cloud](https://console.developers.google.com/apis/library/customsearch.googleapis.com).
2. Asegúrate de estar en el proyecto correcto (arriba a la izquierda).
3. Pulsa **"ENABLE"** (Habilitar) para "Custom Search API".

## Paso 2: Crear el Buscador (CSE)
1. Ve al [Panel de Programmable Search Engine](https://programmablesearchengine.google.com/controlpanel/create).
2. Rellena el formulario:
   - **Name**: `Lead_Enricher`
   - **What to search?**: Selecciona **"Search the entire web"** (Buscar en toda la web).
     - *Nota: Verás una opción "Search specific sites or pages", ignórala por ahora, activaremos "whole web" en el siguiente paso o asegúrate de que esté marcado.*
     - *Si te obliga a poner una web, pon `linkedin.com`.*
   - **Imágenes / SafeSearch**: Desactivados.
   - Pulsa **"CREATE"**.

3. Una vez creado, verás un código. Copia el **"Search engine ID"** (suele empezar por `cx=...` o solo números y letras).
   - Ejemplo: `0123456789:abcdefghijk`

## Paso 3: Configuración Final (Importante)
1. En el menú de la izquierda de tu buscador creado, ve a **"Look and Feel"** > **"All look and feel settings"**. (Opcional, no crítico).
2. Ve a **"Setup"** (Configuración) si no lo estás ya.
3. Asegúrate de que **"Search the entire web"** esté **ACTIVADO** (ON).
   - Si no lo está, actívalo. (Esto es clave para buscar en LinkedIn, InfoCIF, etc.).

## Paso 4: Guardar Credenciales
Añade el ID a tu archivo `.env` (solo añade la línea nueva):

```ini
GOOGLE_PLACES_API_KEY=AIzaSy... (Ya la tienes)
GOOGLE_CSE_ID=tu_search_engine_id_aqui
```
