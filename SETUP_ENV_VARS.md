# Configuración Permanente de Variables de Entorno

## Problema Resuelto
macOS bloquea el acceso de Python al archivo `.env` en el Desktop debido a restricciones de Full Disk Access.

## Solución: Variables de Entorno del Sistema

### Opción 1: Configuración Manual (Recomendada)

1. Abre tu archivo de configuración de shell:
   ```bash
   nano ~/.zshrc
   ```

2. Añade estas líneas al final del archivo:
   ```bash
   # Google API Keys for Lead Generation
   export GOOGLE_PLACES_API_KEY="AIzaSyB9rmQEW1UdtRexvbRmW7-yd7y3AtS9t0s"
   export GOOGLE_CSE_ID="01f2a4cfaf7c04d14"
   ```

3. Guarda el archivo (Ctrl+O, Enter, Ctrl+X)

4. Recarga la configuración:
   ```bash
   source ~/.zshrc
   ```

5. Verifica que funcionó:
   ```bash
   echo $GOOGLE_PLACES_API_KEY
   ```

### Opción 2: Por Sesión (Temporal)

Si solo quieres usar las claves en la sesión actual:
```bash
source set_env.sh
```

## Verificación

Una vez configurado, ejecuta:
```bash
./run_pipeline.sh "arquitectos en Boadilla del Monte" 10
```

El sistema ya no mostrará el error de `.env` y usará las variables de entorno del sistema.

## Notas de Seguridad

- Las API keys están ahora en tu `~/.zshrc`, que es privado de tu usuario
- No compartas este archivo ni lo subas a repositorios públicos
- Si necesitas rotar las keys, edita el `~/.zshrc` y ejecuta `source ~/.zshrc`
