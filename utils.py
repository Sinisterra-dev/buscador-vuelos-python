from datetime import datetime, timedelta

def sumar_dias(fecha_str, dias):
    """Recibe 'YYYY-MM-DD' y devuelve fecha + n días."""
    base = datetime.strptime(fecha_str, "%Y-%m-%d")
    nueva = base + timedelta(days=dias)
    return nueva.strftime("%Y-%m-%d")
