# Arquitectura del Sistema - Diagramas

## 🏗️ Arquitectura General

```mermaid
graph TB
    subgraph "Docker Container"
        N8N[N8N Orchestrator]
        PYTHON[Python Scripts]
        ENV[.env Config]
        
        N8N -->|Execute Command| PYTHON
        PYTHON -->|Read| ENV
    end
    
    subgraph "External Services"
        GPLACES[Google Places API]
        GCSE[Google Custom Search]
        GSHEETS[Google Sheets]
    end
    
    PYTHON -->|Search| GPLACES
    PYTHON -->|Enrich| GCSE
    PYTHON -->|Export| OUTPUT[output/*.csv]
    N8N -->|Upload| GSHEETS
    
    USER[User] -->|Manual Trigger| N8N
    SCHEDULE[Cron Schedule] -->|Auto Trigger| N8N
    
    style N8N fill:#5865F2
    style PYTHON fill:#3776AB
    style GSHEETS fill:#34A853
```

## 🔄 Flujo de Ejecución

```mermaid
sequenceDiagram
    participant User
    participant N8N
    participant Python
    participant GoogleAPI
    participant Output
    participant Sheets

    User->>N8N: Trigger Workflow (Manual/Schedule)
    N8N->>N8N: Set Variables (query, limit)
    N8N->>Python: Execute run_pipeline.sh
    
    Python->>GoogleAPI: Search Places
    GoogleAPI-->>Python: Business Data
    
    Python->>Python: Deduplicate
    Python->>Python: Analyze Pain Points
    Python->>Python: Enrich (LinkedIn)
    
    Python->>Output: Generate CSV
    Output-->>N8N: CSV Path
    
    N8N->>Output: Read CSV
    N8N->>Sheets: Upload Data
    Sheets-->>User: ✅ Complete
```

## 📦 Estructura de Contenedor

```mermaid
graph LR
    subgraph "n8n-lead-generator Container"
        subgraph "Base: n8n:latest"
            N8N_APP[N8N Application]
        end
        
        subgraph "Installed: Python Layer"
            PYTHON3[Python 3]
            PIP[pip packages]
        end
        
        subgraph "Mounted: Project Files"
            SCRIPTS[/data/scripts/]
            ENV_FILE[.env]
            OUTPUT[.tmp/]
        end
        
        N8N_APP --> PYTHON3
        PYTHON3 --> SCRIPTS
        SCRIPTS --> ENV_FILE
        SCRIPTS --> OUTPUT
    end
    
    HOST_OUTPUT[Host: output/] -.->|Volume Mount| OUTPUT
    HOST_ENV[Host: .env] -.->|Volume Mount| ENV_FILE
```

## 🔀 Workflow N8N

```mermaid
graph TD
    START[Schedule Trigger<br/>Every Monday 9AM]
    MANUAL[Manual Trigger<br/>Execute Workflow]
    
    START --> VARS
    MANUAL --> VARS
    
    VARS[Set Variables<br/>query, limit]
    VARS --> EXEC[Execute Pipeline<br/>run_pipeline.sh]
    
    EXEC --> GETCSV[Get Latest CSV Path<br/>ls -t *.csv]
    GETCSV --> CHECK{CSV Exists?}
    
    CHECK -->|Yes| READ[Read CSV Content]
    CHECK -->|No| ERROR[Error Notification]
    
    READ --> PARSE[Parse CSV]
    PARSE --> SHEETS[Upload to Google Sheets]
    SHEETS --> SUCCESS[Success Notification]
    
    style START fill:#34A853
    style MANUAL fill:#4285F4
    style ERROR fill:#EA4335
    style SUCCESS fill:#34A853
```

## 🌐 Despliegue Multi-Plataforma

```mermaid
graph TB
    subgraph "Development (Mac)"
        DEV_DOCKER[Docker Desktop]
        DEV_N8N[N8N Container]
        DEV_DOCKER --> DEV_N8N
    end
    
    subgraph "Production (Windows Server)"
        PROD_DOCKER[Docker Desktop]
        PROD_N8N[N8N Container]
        PROD_DOCKER --> PROD_N8N
    end
    
    subgraph "Client (VPS Cloud)"
        CLOUD_DOCKER[Docker Engine]
        CLOUD_N8N[N8N Container]
        CLOUD_DOCKER --> CLOUD_N8N
    end
    
    GIT[Git Repository] -.->|git clone| DEV_DOCKER
    GIT -.->|git clone| PROD_DOCKER
    GIT -.->|git clone| CLOUD_DOCKER
    
    DEV_N8N -.->|Same Code| PROD_N8N
    PROD_N8N -.->|Same Code| CLOUD_N8N
    
    style GIT fill:#F05032
```

## 🔐 Flujo de Datos y Seguridad

```mermaid
graph LR
    subgraph "Secrets Management"
        ENV[.env File]
        DOCKER_ENV[Docker Environment]
        
        ENV -->|Mounted| DOCKER_ENV
    end
    
    subgraph "Application Layer"
        N8N_VARS[N8N Variables]
        PYTHON_SCRIPTS[Python Scripts]
        
        DOCKER_ENV -->|Injected| N8N_VARS
        DOCKER_ENV -->|Read| PYTHON_SCRIPTS
    end
    
    subgraph "External APIs"
        GAPI[Google APIs]
        
        PYTHON_SCRIPTS -->|Authenticated| GAPI
    end
    
    GITIGNORE[.gitignore] -.->|Excludes| ENV
    
    style ENV fill:#EA4335
    style GITIGNORE fill:#34A853
```

## 📊 Comparación: Antes vs Ahora

```mermaid
graph TB
    subgraph "❌ Arquitectura Anterior (SSH)"
        OLD_N8N[N8N Container]
        OLD_SSH[SSH Connection]
        OLD_HOST[Host Machine]
        OLD_PYTHON[Python Scripts]
        
        OLD_N8N -->|SSH| OLD_SSH
        OLD_SSH -->|Execute| OLD_HOST
        OLD_HOST -->|Run| OLD_PYTHON
    end
    
    subgraph "✅ Arquitectura Nueva (Integrada)"
        NEW_CONTAINER[Single Container]
        NEW_N8N[N8N]
        NEW_PYTHON[Python]
        
        NEW_CONTAINER --> NEW_N8N
        NEW_CONTAINER --> NEW_PYTHON
        NEW_N8N -->|Direct Execute| NEW_PYTHON
    end
    
    style OLD_SSH fill:#EA4335
    style NEW_CONTAINER fill:#34A853
```

---

## 📝 Notas

- **Mermaid**: Estos diagramas se renderizan automáticamente en GitHub
- **Editable**: Puedes modificar los diagramas editando el código Mermaid
- **Documentación Visual**: Útil para presentar a clientes o equipo

---

## 🔗 Referencias

- [Mermaid Documentation](https://mermaid.js.org/)
- [Docker Architecture](https://docs.docker.com/get-started/overview/)
- [N8N Documentation](https://docs.n8n.io/)
