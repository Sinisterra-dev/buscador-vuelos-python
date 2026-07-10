# INSTRUCCIONES DEL PROYECTO

## 1) ¿Qué es este proyecto?

Este proyecto es un buscador de vuelos baratos hecho en Python.
La aplicación recorre todas las fechas de un mes, consulta precios (reales o demo),
ordena resultados por precio y muestra la mejor opción.

## 2) ¿Cómo funciona internamente?

- `main.py`: arranque de la aplicación.
- `gui.py`: interfaz gráfica con PySimpleGUI.
- `api.py`: integración con Amadeus y modo demo.
- `cache.py`: caché SQLite para no repetir búsquedas iguales.
- `utils.py`: utilidades de fechas y formato de precios.
- `tests/test_utils.py`: pruebas unitarias de funciones auxiliares.

Flujo general:
1. Usuario ingresa origen, destino y mes.
2. La app genera todas las fechas del mes.
3. Para cada fecha consulta caché o API.
4. Se guarda en caché, se ordena por precio y se muestra.
5. Se permite exportar resultados a CSV.

## 3) Ejecución local paso a paso

```bash
cd /home/runner/work/buscador-vuelos-python/buscador-vuelos-python
python -m venv venv
source venv/bin/activate   # En Windows usar .\venv\Scripts\Activate.ps1
pip install -r requirements.txt
python main.py
```

## 4) Configurar API real (opcional)

1. Regístrate gratis en https://developers.amadeus.com
2. Crea una app en **My Apps**.
3. Copia `Client ID` y `Client Secret`.
4. Crea `.env` desde `.env.example`.
5. Agrega:

```env
AMADEUS_API_KEY=tu_client_id
AMADEUS_API_SECRET=tu_client_secret
```

Sin `.env`, la app sigue funcionando en modo demo.

## 5) Pruebas

```bash
python -m unittest discover -s tests -v
```

## 6) Demo web gratis accesible para todos

Como esta app es de escritorio, la opción más simple para demo pública es crear
una versión web ligera con Streamlit reutilizando la lógica de `api.py`.

### Opción recomendada: Streamlit Community Cloud (gratis)

1. Crea en el repo un archivo `app_streamlit.py` (interfaz web).
2. Agrega `streamlit` a `requirements.txt`.
3. Sube cambios a GitHub.
4. Ve a https://share.streamlit.io
5. Conecta tu cuenta GitHub.
6. Selecciona este repositorio y rama.
7. Define como archivo principal: `app_streamlit.py`.
8. (Opcional) En *Secrets* agrega `AMADEUS_API_KEY` y `AMADEUS_API_SECRET`.
9. Pulsa **Deploy**.

Resultado: tendrás una URL pública para cualquiera.

### Alternativa gratis

- Hugging Face Spaces (SDK Streamlit) también permite demo pública sin costo.

## 7) Recomendaciones para producción

- Validar límites de uso de API Amadeus.
- Manejar mejor reintentos de red.
- Añadir más pruebas automáticas para `api.py` y `cache.py`.
