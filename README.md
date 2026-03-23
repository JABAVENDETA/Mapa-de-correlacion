# 🇨🇴 Mapa de Impacto del Narcotráfico en Colombia

Dashboard interactivo de análisis geoespacial que visualiza la correlación entre cultivos de coca, violencia, grupos armados, asesinatos y pobreza en Colombia.

![Dashboard Preview](https://img.shields.io/badge/Status-Production%20Ready-brightgreen)
![React](https://img.shields.io/badge/React-19.0.0-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.110.1-green)
![MongoDB](https://img.shields.io/badge/MongoDB-4.5.0-green)

## 🎯 Características Principales

### 📊 Visualización de Datos
- **Mapa interactivo de Colombia** con capas superpuestas
- **5 capas de datos** con colores distintivos y transparencia ajustable:
  - 🌿 Cultivos de Coca (verde lima)
  - 🔥 Violencia (naranja)
  - 👥 Grupos Armados (cian)
  - 💀 Asesinatos (rosa)
  - 💰 Pobreza (amarillo)

### 🔄 Interactividad
- Toggle de capas con un solo click (activar/desactivar)
- Hover sobre regiones para ver tooltips con datos
- Click en regiones para información detallada
- Zoom y navegación del mapa

### 🧠 Análisis de Correlación
- **Detección automática de zonas calientes** basada en convergencia de factores
- **Gráfico de red interactivo** que muestra conexiones entre regiones con factores compartidos
- **Score de riesgo** calculado por región (0-400+)
- **Porcentajes de correlación** entre diferentes factores:
  - Coca + Violencia: 37.5%
  - Coca + Pobreza: 25%
  - Todos los Factores: 18.8%

### 📈 Estadísticas
- Panel de KPIs con totales por categoría
- Gráfico de barras interactivo
- Top 10 zonas de alto riesgo

## 🏗️ Arquitectura

### Stack Tecnológico

**Frontend:**
- React 19.0.0
- React Leaflet (mapas interactivos)
- D3.js (visualización de red)
- Recharts (gráficos)
- TailwindCSS + Shadcn UI (diseño)
- Axios (HTTP client)

**Backend:**
- FastAPI 0.110.1
- Motor (MongoDB async driver)
- Pydantic (validación de datos)

**Base de Datos:**
- MongoDB 4.5.0

## 📁 Estructura del Proyecto

```
/app
├── backend/
│   ├── server.py           # API FastAPI
│   ├── seed_data.py        # Script de inicialización de datos
│   ├── requirements.txt    # Dependencias Python
│   └── .env               # Variables de entorno
├── frontend/
│   ├── src/
│   │   ├── pages/
│   │   │   └── Dashboard.js
│   │   ├── components/
│   │   │   ├── MapComponent.js
│   │   │   ├── LeftPanel.js
│   │   │   ├── RightPanel.js
│   │   │   ├── CorrelationPanel.js
│   │   │   ├── NetworkGraph.js
│   │   │   └── LayerToggle.js
│   │   ├── App.js
│   │   └── index.css
│   ├── package.json
│   └── .env               # Variables de entorno
└── design_guidelines.json  # Guías de diseño

```

## 🚀 Instalación y Configuración

### Prerequisitos
- Node.js 16+
- Python 3.9+
- MongoDB 4.5+
- Yarn

### 1. Clonar el Repositorio

```bash
git clone <repository-url>
cd narco-impact-map
```

### 2. Configurar Backend

```bash
cd backend

# Crear entorno virtual
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt

# Configurar variables de entorno
cp .env.example .env
# Editar .env con tus configuraciones
```

### 3. Configurar Frontend

```bash
cd frontend

# Instalar dependencias
yarn install

# Configurar variables de entorno
cp .env.example .env
# Editar .env con la URL de tu backend
```

### 4. Inicializar Base de Datos

```bash
cd backend
python seed_data.py
```

Este comando poblará MongoDB con datos mock basados en fuentes públicas (UNODC, DANE).

### 5. Ejecutar la Aplicación

**Backend:**
```bash
cd backend
uvicorn server:app --reload --host 0.0.0.0 --port 8001
```

**Frontend:**
```bash
cd frontend
yarn start
```

La aplicación estará disponible en `http://localhost:3000`

## 🔌 API Endpoints

### Capas de Datos
- `GET /api/layers/{layer_type}` - Obtener datos GeoJSON de una capa específica
  - layer_type: `coca`, `violence`, `armed_groups`, `murders`, `poverty`

### Estadísticas
- `GET /api/stats` - Obtener estadísticas de todas las capas
- `GET /api/stats/{layer_type}` - Obtener estadísticas de una capa específica

### Regiones
- `GET /api/region/{region_name}` - Obtener todos los datos de una región específica

### Análisis de Correlación
- `GET /api/correlation/analysis` - Análisis completo de correlaciones y zonas calientes

## 📊 Fuentes de Datos

Los datos utilizados están basados en información pública de:
- **UNODC** (Oficina de las Naciones Unidas contra la Droga y el Delito)
- **DANE** (Departamento Administrativo Nacional de Estadística)
- **Gobierno de Colombia** (reportes oficiales de seguridad)

⚠️ **Nota:** Los datos actuales son MOCK/simulados basados en patrones conocidos. Para producción, se deben integrar APIs reales de estas fuentes.

## 🎨 Diseño

El dashboard sigue un diseño **Swiss & High-Contrast** con:
- Tema oscuro profesional
- Paneles flotantes con glass-morphism
- Tipografías: Chivo (headings), IBM Plex Sans (body), JetBrains Mono (stats)
- Colores cuidadosamente seleccionados para máxima distinción entre capas
- Transparencia ajustada para visualización de superposición óptima

## 🔧 Configuración Avanzada

### Variables de Entorno

**Backend (.env):**
```env
MONGO_URL=mongodb://localhost:27017
DB_NAME=colombia_narco_map
CORS_ORIGINS=*
```

**Frontend (.env):**
```env
REACT_APP_BACKEND_URL=http://localhost:8001
```

### Personalización de Capas

Para agregar o modificar capas, edita:
1. `backend/seed_data.py` - Datos y geometrías
2. `frontend/src/components/MapComponent.js` - Colores y estilos
3. `backend/server.py` - Endpoints API

## 🧪 Testing

```bash
# Backend
cd backend
pytest

# Frontend
cd frontend
yarn test
```

## 📦 Deployment

### Opción 1: Emergent Platform
La aplicación está lista para deployment en Emergent Platform con configuración automática.

### Opción 2: Manual

**Backend:**
```bash
gunicorn -w 4 -k uvicorn.workers.UvicornWorker server:app
```

**Frontend:**
```bash
yarn build
# Servir carpeta build/ con nginx o similar
```

## 🤝 Contribuciones

Las contribuciones son bienvenidas! Por favor:
1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📝 Roadmap

- [ ] Integración con APIs públicas en tiempo real
- [ ] Filtros temporales para análisis histórico
- [ ] Exportación de reportes en PDF
- [ ] Sistema de notificaciones para cambios en zonas calientes
- [ ] Predicciones basadas en ML
- [ ] Autenticación de usuarios
- [ ] Dashboard administrativo

## 📄 Licencia

Este proyecto está bajo la Licencia MIT - ver el archivo [LICENSE](LICENSE) para más detalles.

## 👥 Autores

- **Desarrollado con Emergent AI** - [emergent.sh](https://emergent.sh)

## 🙏 Agradecimientos

- UNODC por datos de cultivos de coca
- DANE por estadísticas socioeconómicas
- Gobierno de Colombia por datos de seguridad
- Comunidad open source por las increíbles librerías utilizadas

---

**⚠️ Disclaimer:** Esta herramienta es solo para fines de análisis y visualización de datos. Los datos mostrados son aproximaciones basadas en fuentes públicas y no deben ser utilizados como fuente única para toma de decisiones críticas.
