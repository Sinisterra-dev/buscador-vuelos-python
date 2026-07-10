"""Punto de entrada de la aplicación."""

import logging
from gui import start_gui

if __name__ == "__main__":
    # Configuramos logs simples para poder ver errores y estado de la app.
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s"
    )
    # Mensaje inicial para confirmar que el arranque empezó correctamente.
    logging.info("Iniciando app de vuelos...")
    # Lanzamos la interfaz gráfica principal.
    start_gui()
