# Guía de Configuración SSH - N8N Docker (Windows) a Host

**Propósito:** Permitir que N8N ejecutándose en Docker en Windows pueda ejecutar comandos en el host vía SSH.

## Tu Configuración
- **Servidor (24/7):** Windows con Docker Desktop
- **Desarrollo:** Mac (tu ordenador de trabajo)
- **N8N:** Ejecutándose en Docker en el servidor Windows
- **Scripts Python:** En el servidor Windows

---

## Paso 1: Habilitar SSH en Windows (Host)

### Opción A: OpenSSH Nativo de Windows (RECOMENDADO)

1. Abre **PowerShell como Administrador**
2. Ejecuta:

```powershell
# Instalar OpenSSH Server
Add-WindowsCapability -Online -Name OpenSSH.Server~~~~0.0.1.0

# Iniciar el servicio
Start-Service sshd

# Configurar inicio automático
Set-Service -Name sshd -StartupType 'Automatic'

# Verificar que está corriendo
Get-Service sshd
```

**Salida esperada:** `Status: Running`

3. **Configurar Firewall:**
```powershell
# Permitir SSH en el firewall (puerto 22)
New-NetFirewallRule -Name sshd -DisplayName 'OpenSSH Server (sshd)' -Enabled True -Direction Inbound -Protocol TCP -Action Allow -LocalPort 22
```

4. **Verificar tu usuario:**
```powershell
whoami
# Anota el resultado, lo necesitarás (ej: DESKTOP-ABC\Guille)
```

### Opción B: SSH en WSL2 (Si usas WSL)

Si tus scripts están en WSL2 (Ubuntu):

```bash
# Dentro de WSL2
sudo apt update
sudo apt install openssh-server
sudo service ssh start

# Configurar inicio automático
sudo systemctl enable ssh
```

---

## Paso 2: Generar Clave SSH Dentro del Contenedor N8N

### 2.1 Acceder al Contenedor N8N
```powershell
# En PowerShell o CMD en Windows
docker exec -it <nombre_contenedor_n8n> /bin/sh
```

Para encontrar el nombre de tu contenedor:
```powershell
docker ps | findstr n8n
```

### 2.2 Generar Par de Claves SSH
```bash
# Dentro del contenedor N8N
mkdir -p ~/.ssh
ssh-keygen -t ed25519 -C "n8n-automation" -f ~/.ssh/id_n8n -N ""
```

Esto crea:
- `~/.ssh/id_n8n` (clave privada - permanece en el contenedor)
- `~/.ssh/id_n8n.pub` (clave pública - copiar al host Windows)

### 2.3 Mostrar la Clave Pública
```bash
cat ~/.ssh/id_n8n.pub
```

**Copia toda la salida** (comienza con `ssh-ed25519`).

---

## Paso 3: Añadir la Clave Pública al Host Windows

### Si usas OpenSSH Nativo de Windows:

1. En Windows, abre **PowerShell**
2. Crea el directorio `.ssh` si no existe:

```powershell
# Crear directorio .ssh en tu perfil de usuario
New-Item -Path "$env:USERPROFILE\.ssh" -ItemType Directory -Force

# Crear archivo authorized_keys
New-Item -Path "$env:USERPROFILE\.ssh\authorized_keys" -ItemType File -Force
```

3. Abre el archivo `authorized_keys` con Notepad:
```powershell
notepad "$env:USERPROFILE\.ssh\authorized_keys"
```

4. **Pega la clave pública** del Paso 2.3 (toda la línea `ssh-ed25519 AAAA...`)
5. Guarda y cierra

6. **Configurar permisos (IMPORTANTE):**
```powershell
# Deshabilitar herencia
icacls "$env:USERPROFILE\.ssh\authorized_keys" /inheritance:r

# Dar permisos solo al usuario actual y SYSTEM
icacls "$env:USERPROFILE\.ssh\authorized_keys" /grant:r "$env:USERNAME:F"
icacls "$env:USERPROFILE\.ssh\authorized_keys" /grant:r "SYSTEM:F"
```

### Si usas WSL2:

```bash
# Dentro de WSL2
mkdir -p ~/.ssh
chmod 700 ~/.ssh

# Añadir la clave pública
echo "ssh-ed25519 AAAA... n8n-automation" >> ~/.ssh/authorized_keys
chmod 600 ~/.ssh/authorized_keys
```

---

## Paso 4: Probar Conexión SSH desde el Contenedor N8N

### 4.1 Probar Conectividad al Host

Desde **dentro del contenedor N8N**:

```bash
# Docker Desktop en Windows usa host.docker.internal
ping host.docker.internal
```

### 4.2 Probar Conexión SSH

**Si usas OpenSSH Nativo de Windows:**
```bash
# Dentro del contenedor N8N
ssh -i ~/.ssh/id_n8n <tu_usuario_windows>@host.docker.internal whoami
```

Reemplaza `<tu_usuario_windows>` con tu usuario de Windows (ej: `Guille`).

**Si usas WSL2:**
```bash
# Primero necesitas la IP de WSL2
# En Windows PowerShell:
wsl hostname -I

# Luego en el contenedor N8N:
ssh -i ~/.ssh/id_n8n <usuario_wsl>@<ip_wsl> whoami
```

**Salida esperada:** Tu nombre de usuario

⚠️ **Si te pide contraseña:** La clave SSH no se configuró correctamente. Repite el Paso 3.

### 4.3 Probar Ejecución del Pipeline

**Importante:** Necesitas saber dónde están tus scripts.

**Si los scripts están en Windows:**
```bash
# Dentro del contenedor N8N
ssh -i ~/.ssh/id_n8n <usuario>@host.docker.internal \
  "cd C:\Users\Guille\Desktop\Antigravity\01_PROJECTS\Buscador-Rate-Leads && bash run_pipeline.sh 'test' 5"
```

**Si los scripts están en WSL2:**
```bash
ssh -i ~/.ssh/id_n8n <usuario>@<ip_wsl> \
  "cd /home/guille/Buscador-Rate-Leads && bash run_pipeline.sh 'test' 5"
```

---

## Paso 5: Configurar Credenciales SSH en N8N

1. Abre la UI de N8N → **Credentials** → **New**
2. Selecciona **SSH**
3. Configura:
   - **Host:** `host.docker.internal` (o IP de WSL2)
   - **Port:** `22`
   - **Username:** Tu usuario de Windows o WSL
   - **Private Key:** Pega el contenido de `~/.ssh/id_n8n` del contenedor
   - **Passphrase:** Dejar vacío

4. **Test** la conexión
5. **Save** como "Host SSH Access"

---

## Paso 6: Actualizar Rutas en el Workflow de N8N

Debes actualizar las rutas en `n8n_pipeline_workflow.json` según dónde estén tus scripts:

### Si los scripts están en Windows:

```json
{
  "command": "cd C:\\Users\\Guille\\Desktop\\Antigravity\\01_PROJECTS\\Buscador-Rate-Leads && bash run_pipeline.sh \"{{ $json.query }}\" {{ $json.limit }}"
}
```

### Si los scripts están en WSL2:

```json
{
  "command": "cd /home/guille/Buscador-Rate-Leads && bash run_pipeline.sh \"{{ $json.query }}\" {{ $json.limit }}"
}
```

---

## Consideraciones Especiales para Windows

### 1. Git Bash o WSL para ejecutar `run_pipeline.sh`

El script `run_pipeline.sh` es un script Bash. En Windows necesitas:

**Opción A - WSL2 (RECOMENDADO):**
- Mueve todo el proyecto a WSL2
- Ejecuta desde WSL2

**Opción B - Git Bash:**
- Asegúrate de que Git Bash está instalado
- Usa `bash` explícitamente en los comandos SSH

### 2. Python en Windows vs WSL

Verifica dónde está instalado Python:

**En Windows:**
```powershell
python --version
# o
python3 --version
```

**En WSL2:**
```bash
python3 --version
```

Asegúrate de que todas las dependencias (`requirements.txt`) están instaladas en el entorno correcto.

### 3. Variables de Entorno

El archivo `.env` debe estar en la ubicación correcta:
- **Windows:** `C:\Users\Guille\Desktop\Antigravity\01_PROJECTS\Buscador-Rate-Leads\.env`
- **WSL2:** `/home/guille/Buscador-Rate-Leads/.env`

---

## Solución de Problemas Específicos de Windows

### "Permission denied (publickey)"
```powershell
# Verificar permisos del archivo authorized_keys
icacls "$env:USERPROFILE\.ssh\authorized_keys"

# Debería mostrar solo tu usuario y SYSTEM
# Si hay otros, elimínalos:
icacls "$env:USERPROFILE\.ssh\authorized_keys" /inheritance:r
icacls "$env:USERPROFILE\.ssh\authorized_keys" /grant:r "$env:USERNAME:F"
```

### "Connection refused"
```powershell
# Verificar que SSH está corriendo
Get-Service sshd

# Si está detenido, iniciarlo
Start-Service sshd
```

### "bash: command not found"
- Instala Git Bash o usa WSL2
- O convierte `run_pipeline.sh` a un script PowerShell

---

## Recomendación Final

Para tu caso específico, te recomiendo:

1. **Usar WSL2** en el servidor Windows
2. **Mover todo el proyecto a WSL2** (`/home/guille/Buscador-Rate-Leads`)
3. **Ejecutar Python desde WSL2**
4. **N8N en Docker Desktop** (Windows) conecta vía SSH a WSL2

**Ventajas:**
- ✅ Entorno Linux completo (más compatible con scripts Bash)
- ✅ Mejor rendimiento para Python
- ✅ Más fácil de mantener
- ✅ Mismo entorno que producción (si migras a cloud)

---

## Verificación Final

Antes de continuar, asegúrate de que:
- ✅ SSH está habilitado en Windows (o WSL2)
- ✅ Puedes ejecutar `whoami` desde el contenedor N8N vía SSH
- ✅ Puedes ejecutar `run_pipeline.sh` desde el contenedor N8N vía SSH
- ✅ Python y todas las dependencias están instaladas
- ✅ El archivo `.env` está en la ubicación correcta
- ✅ Las credenciales SSH están configuradas en N8N

Si todos los puntos están verificados, estás listo para importar el workflow.
