from datetime import datetime, timedelta


def sumar_dias(fecha_str, dias):
    """Recibe 'YYYY-MM-DD' y devuelve la fecha desplazada n días."""
    # Convertimos texto a fecha.
    base = datetime.strptime(fecha_str, "%Y-%m-%d")
    # Sumamos la cantidad de días solicitada.
    nueva = base + timedelta(days=dias)
    # Volvemos a texto para mantener formato consistente en toda la app.
    return nueva.strftime("%Y-%m-%d")


def normalizar_precio(valor):
    """Convierte un string a float. Retorna 0.0 si no es válido."""
    try:
        return float(valor)
    except (ValueError, TypeError):
        return 0.0


def formatear_precio_cop(precio):
    """Formatea un número como precio en pesos colombianos. Ej: 450000 → '$450.000 COP'"""
    try:
        return f"${int(precio):,.0f} COP".replace(",", ".")
    except (ValueError, TypeError):
        return "$0 COP"
