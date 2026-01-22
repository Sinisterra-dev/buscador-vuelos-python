# 🛫 Buscador de Vuelos Baratos (CLO ↔ CTG)

Aplicación de escritorio desarrollada en **Python** para buscar y comparar vuelos baratos entre **Cali (CLO)** y **Cartagena (CTG)**.  
Permite analizar precios de todo un mes, identificar el vuelo más económico y exportar los resultados a CSV.  
Funciona tanto con la **API real de Amadeus** como en **modo demo (mock)**, mostrando precios en **pesos colombianos (COP)**.

---

## ✨ Características

- 🔍 Búsqueda de vuelos por mes completo  
- 🔁 Soporte para **solo ida** o **ida y vuelta**  
- 📆 Evaluación automática de regresos entre **11 y 15 días**  
- 💰 Orden automático del más barato al más caro  
- 🪄 Resaltado del vuelo más económico del mes  
- 📤 Exportación de resultados a archivo **CSV**  
- ⚡ Sistema de **caché** en SQLite para evitar consultas repetidas  
- 🧩 Interfaz gráfica sencilla y funcional (PySimpleGUI)  
- 🧱 Modo **mock** sin necesidad de claves API  

---

## 🧰 Tecnologías utilizadas

- **Python 3.10+**
- **PySimpleGUI**
- **Pandas**
- **Requests**
- **SQLite3**
- **Amadeus API** (opcional)
- **Variables de entorno (.env)**

---

## 🚀 Instalación (Windows / PowerShell)

1. Clonar el repositorio y acceder a la carpeta del proyecto:

   ```powershell
   git clone <tu_repositorio>
   cd buscador_vuelos

python -m venv venv
.\venv\Scripts\Activate.ps1

2. Instalar las dependencias necesarias:
    ```powershell
   pip install -r requirements.txt
