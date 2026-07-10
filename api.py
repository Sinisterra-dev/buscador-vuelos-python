import os
import requests
import logging
import calendar
from datetime import date
from dotenv import load_dotenv

# Cargamos variables del archivo .env al iniciar el módulo.
load_dotenv()

# Credenciales de Amadeus (si no existen, la app entra en modo demo).
AMADEUS_API_KEY = os.getenv("AMADEUS_API_KEY")
AMADEUS_API_SECRET = os.getenv("AMADEUS_API_SECRET")

# Endpoints del entorno de pruebas de Amadeus.
AMADEUS_URL_TOKEN = "https://test.api.amadeus.com/v1/security/oauth2/token"
AMADEUS_URL_FLIGHTS = "https://test.api.amadeus.com/v2/shopping/flight-offers"

# Aerolíneas activas en rutas domésticas colombianas
AEROLINEAS_DEMO = [
    ("Avianca", "https://www.avianca.com"),
    ("LATAM", "https://www.latam.com"),
    ("Wingo", "https://www.wingo.com"),
    ("JetSmart", "https://www.jetsmart.com"),
]


def get_access_token():
    """Solicita un token OAuth2 para consultar la API real."""
    if not AMADEUS_API_KEY or not AMADEUS_API_SECRET:
        logging.warning("No hay API key configurada. Usando modo demo.")
        return None
    data = {
        "grant_type": "client_credentials",
        "client_id": AMADEUS_API_KEY,
        "client_secret": AMADEUS_API_SECRET,
    }
    try:
        resp = requests.post(AMADEUS_URL_TOKEN, data=data, timeout=10)
        if resp.status_code != 200:
            logging.error("Error obteniendo token Amadeus")
            return None
        return resp.json().get("access_token")
    except Exception as e:
        logging.error(f"Error de conexión al obtener token: {e}")
        return None


def buscar_vuelos(origen, destino, fecha_salida, fecha_vuelta=None):
    """
    Busca vuelos y devuelve resultados normalizados.

    Si no hay credenciales o falla la API, devuelve datos simulados.
    """
    token = get_access_token()
    if token is None:
        return mock_vuelos(origen, destino, fecha_salida, fecha_vuelta)

    # Parámetros principales de búsqueda.
    params = {
        "originLocationCode": origen,
        "destinationLocationCode": destino,
        "departureDate": fecha_salida,
        "adults": 1,
        "currencyCode": "COP",
        "max": 3,
    }
    if fecha_vuelta:
        params["returnDate"] = fecha_vuelta

    headers = {"Authorization": f"Bearer {token}"}
    try:
        resp = requests.get(AMADEUS_URL_FLIGHTS, params=params, headers=headers, timeout=15)
        resp.raise_for_status()
    except Exception as e:
        # Si falla la API, mantenemos la app usable con datos demo.
        logging.warning(f"Error al consultar API ({e}), usando mock.")
        return mock_vuelos(origen, destino, fecha_salida, fecha_vuelta)

    data = resp.json()
    vuelos = []
    for item in data.get("data", []):
        # Amadeus entrega precio como texto; lo convertimos a número.
        precio = float(item["price"]["total"])
        itinerarios = item["itineraries"]
        # Primer segmento del primer itinerario = salida.
        salida = itinerarios[0]["segments"][0]["departure"]["at"].split("T")[0]
        # Último segmento del último itinerario = llegada de regreso.
        vuelta = itinerarios[-1]["segments"][-1]["arrival"]["at"].split("T")[0] if len(itinerarios) > 1 else None
        # Código de aerolínea validadora.
        aerolinea = item["validatingAirlineCodes"][0]
        vuelos.append({
            "aerolinea": aerolinea,
            "precio": precio,
            "salida": salida,
            "vuelta": vuelta,
            "enlace": "https://www.google.com/flights",
        })
    return vuelos


def mock_vuelos(origen, destino, salida, vuelta):
    """Modo demo: genera resultados simulados con rangos realistas en COP."""
    import random
    # Precios típicos de vuelos domésticos en Colombia (en COP)
    precios = [round(random.uniform(180_000, 650_000), -3) for _ in range(len(AEROLINEAS_DEMO))]
    return [
        {
            "aerolinea": nombre,
            "precio": precio,
            "salida": salida,
            "vuelta": vuelta or salida,
            "enlace": url,
        }
        for (nombre, url), precio in zip(AEROLINEAS_DEMO, precios)
    ]


def es_modo_demo():
    """Retorna True si la aplicación está funcionando en modo demo (sin API key)."""
    return not (AMADEUS_API_KEY and AMADEUS_API_SECRET)


def generar_fechas_mes(mes_str):
    """Genera todas las fechas (YYYY-MM-DD) de un mes dado."""
    anio, mes = map(int, mes_str.split("-"))
    _, ultimo_dia = calendar.monthrange(anio, mes)
    return [date(anio, mes, dia).isoformat() for dia in range(1, ultimo_dia + 1)]
