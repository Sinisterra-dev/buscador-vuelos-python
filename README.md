# ✈️ Buscador de Vuelos Baratos

Aplicación de escritorio desarrollada en **Python** para buscar y comparar vuelos baratos en rutas domésticas de Colombia (por defecto **Cali ↔ Cartagena**).

Analiza los precios de un mes completo, identifica el vuelo más económico y permite exportar los resultados a CSV. Funciona tanto con la **API real de Amadeus** como en **modo demo** (sin necesidad de claves), mostrando precios en **pesos colombianos (COP)**.

---

## ✨ Características

| # | Funcionalidad |
|---|---------------|
| 🔍 | Búsqueda de vuelos por mes completo |
| 🔁 | Soporte para **solo ida** o **ida y vuelta** |
| 📆 | Evaluación automática de regresos entre **11 y 15 días** |
| 💰 | Orden automático del más barato al más caro |
| 🪄 | Resaltado del vuelo más económico en la barra de estado |
| 📤 | Exportación a **CSV** con timestamp en el nombre del archivo |
| ⚡ | Caché en **SQLite** para evitar consultas repetidas |
| 🖥️ | Interfaz gráfica moderna con **PySimpleGUI** |
| 🔗 | Clic en fila abre el enlace de compra en el navegador |
| 🧩 | **Modo demo** sin necesidad de claves API |
| ✅ | Validación de entradas con mensajes de error claros |

---

## 🧱 Modo Demo vs. API Real

La aplicación detecta automáticamente si hay credenciales configuradas:

| | Modo Demo | API Real |
|---|---|---|
| **Requiere registro** | ❌ No | ✅ Sí (gratis en Amadeus) |
| **Datos** | Precios simulados en COP | Precios en tiempo real |
| **Aerolíneas** | Avianca, LATAM, Wingo, JetSmart | Todas las disponibles |
| **Banner** | 🟠 Naranja — aviso visible | 🟢 Verde — conectado |

> **En modo demo** los precios son generados aleatoriamente dentro de rangos realistas para vuelos domésticos colombianos (COP 180.000 – 650.000). Son útiles para explorar la interfaz y evaluar la herramienta.

---

## 🧰 Tecnologías utilizadas

- **Python 3.10+**
- **PySimpleGUI** — interfaz gráfica de escritorio
- **Pandas** — procesamiento y exportación de datos
- **Requests** — llamadas HTTP a la API de Amadeus
- **SQLite3** — caché local de resultados
- **python-dotenv** — gestión de variables de entorno
- **Amadeus API** — fuente de datos de vuelos reales (opcional)

---

## 🚀 Instalación

### Requisitos previos

- Python 3.10 o superior
- `pip` actualizado

### Pasos

```bash
# 1. Clonar el repositorio
git clone https://github.com/Sinisterra-dev/buscador-vuelos-python.git
cd buscador-vuelos-python

# 2. Crear y activar el entorno virtual
python -m venv venv

# Windows (PowerShell)
.\venv\Scripts\Activate.ps1

# macOS / Linux
source venv/bin/activate

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Configurar variables de entorno (opcional — sin esto funciona en modo demo)
cp .env.example .env
# Edita .env y añade tus credenciales de Amadeus

# 5. Ejecutar la aplicación
python main.py
```

---

## 🔑 Obtener credenciales de Amadeus (opcional)

1. Regístrate gratis en [developers.amadeus.com](https://developers.amadeus.com)
2. Ve a **My Apps** → **Create new app**
3. Copia el **Client ID** y el **Client Secret**
4. Pégalos en tu archivo `.env`:

```env
AMADEUS_API_KEY=tu_client_id_aqui
AMADEUS_API_SECRET=tu_client_secret_aqui
```

> La API de pruebas (*test environment*) de Amadeus es gratuita y no requiere tarjeta de crédito.

---

## 🖥️ Uso de la aplicación

1. Introduce los códigos IATA de **Origen** y **Destino** (ej: `CLO` → `CTG`)
2. Introduce el mes en formato `YYYY-MM` (ej: `2026-05`)
3. Selecciona el modo: **Solo ida** o **Ida y vuelta**
4. Haz clic en **🔍 Buscar**
5. Los resultados aparecen ordenados de menor a mayor precio
6. Haz clic en cualquier fila para abrir el sitio de la aerolínea
7. Usa **📤 Exportar CSV** para guardar los resultados

---

## 🗂️ Estructura del proyecto

```
buscador-vuelos-python/
├── main.py          # Punto de entrada — inicia la GUI
├── gui.py           # Interfaz gráfica (PySimpleGUI)
├── api.py           # Lógica de búsqueda: API real + modo demo
├── cache.py         # Caché SQLite para evitar llamadas duplicadas
├── utils.py         # Funciones auxiliares (fechas, formato de precios)
├── requirements.txt # Dependencias del proyecto
├── .env.example     # Plantilla de configuración de variables de entorno
├── tests/
│   └── test_utils.py  # Tests unitarios de utilidades
└── data/
    └── cache.db     # Base de datos SQLite (se crea automáticamente)
```

---

## 🧪 Tests

```bash
python -m pytest tests/ -v
```

---

## 📄 Licencia

Este proyecto está bajo la licencia **MIT**. Consulta el archivo [LICENSE](LICENSE) para más detalles.

---

## 🙌 Contribuciones

Las contribuciones son bienvenidas. Si encuentras un bug o tienes una idea de mejora, abre un *issue* o envía un *pull request*.

