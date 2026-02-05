# Guía de Uso del Sistema de Leads

## Flujo de Trabajo (Paso a Paso)

Este documento explica cómo usar el sistema "infalible" para generar clientes potenciales.

---

### Opción A: Ejecución en 1-Click (Recomendado)
Usa el script automático que hace todo (buscar, limpiar, fotos y exportar):

```bash
./run_pipeline.sh "abogados en Vigo" 20
```

1. Busca leads en Google
2. Elimina duplicados
3. Toma capturas de pantalla
4. Crea el archivo para HubSpot

*Output Final: `.tmp/hubspot_import_[fecha].csv`*

---

### Opción B: Ejecución Manual Paso a Paso
Si prefieres controlar cada paso:

#### Paso 1: Buscar
```bash
python execution/scrape_gmb_api.py --query "abogados en Vigo" --max-results 20
```

#### Paso 2: Limpieza y Visuales
```bash
# 2.1. Eliminar duplicados
python execution/deduplicate_leads.py --input .tmp/api_leads_[fecha].json --output .tmp/leads_clean.json

# 2.2. Capturar Screenshots
python execution/capture_screenshots.py --input .tmp/leads_clean.json
```

#### Paso 3: Exportar para HubSpot
```bash
python execution/export_to_hubspot_csv.py --input .tmp/leads_clean.json --output .tmp/hubspot_import.csv
```

---

### Paso 4: Cierre en HubSpot
1. Ve a **Contacts** > **Import**.
2. Sube el archivo `hubspot_import.csv`.
3. Verás que las columnas se mapean solas (Name -> Company Name, etc.).
4. ¡Listo! Ya puedes llamar o enviar correos.

---

### Mantenimiento
- **Costos**: Recuerda que tienes $200 gratis en Google Cloud. Vigila tu consola si haces más de 5,000 búsquedas al mes.
- **Limpieza**: Borra la carpeta `.tmp` periódicamente si se llena mucho.
