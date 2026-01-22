import os
import requests
import logging
import calendar
from datetime import date
from dotenv import load_dotenv

load_dotenv()

AMADEUS_API_KEY = os.getenv("AMADEUS_API_KEY")
AMADEUS_API_SECRET = os.getenv("AMADEUS_API_SECRET")

AMADEUS_URL_TOKEN = "https://test.api.amadeus.com/v1/security/oauth2/token"
AMADEUS_URL_FLIGHTS = "https://test.api.amadeus.com/v2/shopping/flight-offers"


def get_access_token():
    if not AMADEUS_API_KEY or not AMADEUS_API_SECRET:
        logging.warning("No hay API key configurada. Usando modo demo.")
        return None
    data = {
        "grant_type": "client_credentials",
        "client_id": AMADEUS_API_KEY,
        "client_secret": AMADEUS_API_SECRET,
    }
    resp = requests.post(AMADEUS_URL_TOKEN, data=data)
    if resp.status_code != 200:
        logging.error("Error obteniendo token Amadeus")
        return None
    return resp.json().get("access_token")


def buscar_vuelos(origen, destino, fecha_salida, fecha_vuelta=None):
    """Busca vuelos reales o mock si no hay API key."""
    token = get_access_token()
    if token is None:
        return mock_vuelos(origen, destino, fecha_salida, fecha_vuelta)

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
        logging.warning(f"Error al consultar API ({e}), usando mock.")
        return mock_vuelos(origen, destino, fecha_salida, fecha_vuelta)

    data = resp.json()
    vuelos = []
    for item in data.get("data", []):
        precio = float(item["price"]["total"])
        itinerarios = item["itineraries"]
        salida = itinerarios[0]["segments"][0]["departure"]["at"].split("T")[0]
        vuelta = itinerarios[-1]["segments"][-1]["arrival"]["at"].split("T")[0] if len(itinerarios) > 1 else None
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
    """Modo demo: datos simulados pero con precio aleatorio para variedad."""
    import random
    precios = [round(random.uniform(120, 400), 2) for _ in range(3)]
    return [
        {"aerolinea": "Avianca", "precio": precios[0], "salida": salida, "vuelta": vuelta or salida, "enlace": "https://www.avianca.com"},
        {"aerolinea": "LATAM", "precio": precios[1], "salida": salida, "vuelta": vuelta or salida, "enlace": "https://www.latam.com"},
        {"aerolinea": "Viva Air", "precio": precios[2], "salida": salida, "vuelta": vuelta or salida, "enlace": "https://www.vivaair.com"},
    ]


def generar_fechas_mes(mes_str):
    """Genera todas las fechas (YYYY-MM-DD) de un mes dado."""
    anio, mes = map(int, mes_str.split("-"))
    _, ultimo_dia = calendar.monthrange(anio, mes)
    return [date(anio, mes, dia).isoformat() for dia in range(1, ultimo_dia + 1)]
