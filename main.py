import logging
from gui import start_gui

if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s"
    )
    logging.info("Iniciando app de vuelos...")
    start_gui()
