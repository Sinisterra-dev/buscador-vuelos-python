# ✈️ Buscador de Vuelos Baratos (Python)

Aplicación de escritorio en Python para buscar vuelos económicos por mes completo.

- Funciona **sin claves** en modo demo.
- Usa **API real de Amadeus** cuando configuras credenciales.
- Ordena resultados de menor a mayor precio para encontrar el más barato.

---

## ✅ Qué debes hacer exactamente para que funcione

```bash
# 1) Entrar al proyecto
cd /home/runner/work/buscador-vuelos-python/buscador-vuelos-python

# 2) Crear entorno virtual
python -m venv venv

# 3) Activarlo
# Linux/macOS:
source venv/bin/activate
# Windows PowerShell:
# .\venv\Scripts\Activate.ps1

# 4) Instalar dependencias
pip install -r requirements.txt

# 5) (Opcional) configurar API real
cp .env.example .env
# Edita .env y agrega AMADEUS_API_KEY y AMADEUS_API_SECRET

# 6) Ejecutar
python main.py
```

Si no configuras `.env`, la app **igual funciona** en modo demo con precios simulados realistas en COP.

---

## 🔍 Cómo encontrar vuelos baratos en la app

1. Escribe Origen y Destino IATA (ejemplo: `CLO` → `CTG`).
2. Escribe el mes en formato `YYYY-MM` (ejemplo: `2026-08`).
3. Elige **Solo ida** o **Ida y vuelta**.
4. Pulsa **🔍 Buscar**.
5. Revisa la tabla ordenada: el primer resultado es el más económico.
6. Puedes exportar con **📤 Exportar CSV**.

---

## 🧪 Probar que está bien instalado

```bash
python -m unittest discover -s tests -v
```

---

## 🧱 Estructura del proyecto

```text
buscador-vuelos-python/
├── main.py
├── gui.py
├── api.py
├── cache.py
├── utils.py
├── requirements.txt
├── .env.example
├── INSTRUCCIONES.md
└── tests/
    └── test_utils.py
```

---

## 🌐 Despliegue / demo web gratis

Consulta `INSTRUCCIONES.md`, sección **“Demo web gratis accesible para todos”**.

---

## 📄 Licencia

MIT. Ver `LICENSE`.
