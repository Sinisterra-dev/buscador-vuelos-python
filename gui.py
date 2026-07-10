"""Interfaz gráfica principal del buscador de vuelos."""

import logging
from datetime import datetime
import PySimpleGUI as sg
import pandas as pd
from api import buscar_vuelos, generar_fechas_mes, es_modo_demo
from utils import sumar_dias, formatear_precio_cop
from cache import guardar_cache, cargar_cache

# ─── Constantes visuales ────────────────────────────────────────────────────
THEME = "LightBlue"
FONT_TITLE = ("Helvetica", 13, "bold")
FONT_NORMAL = ("Helvetica", 10)
COL_ANCHO = [14, 16, 12, 12, 35]
HEADINGS = ["Aerolínea", "Precio (COP)", "Salida", "Vuelta", "Enlace"]


def _banner_demo():
    """Devuelve una fila de advertencia si se está en modo demo."""
    if es_modo_demo():
        return [sg.Text(
            "⚠️  MODO DEMO — los precios son simulados. Configura tu API key para datos reales.",
            text_color="white",
            background_color="#E65100",
            font=FONT_NORMAL,
            expand_x=True,
            pad=(6, 4),
        )]
    return [sg.Text(
        "✅  Conectado a Amadeus API — datos en tiempo real.",
        text_color="white",
        background_color="#2E7D32",
        font=FONT_NORMAL,
        expand_x=True,
        pad=(6, 4),
    )]


def _validar_inputs(origen, destino, mes):
    """Valida los campos de entrada. Devuelve (True, '') o (False, mensaje_error)."""
    if len(origen) != 3 or not origen.isalpha():
        return False, "El código de origen debe ser un código IATA de 3 letras (ej: CLO)."
    if len(destino) != 3 or not destino.isalpha():
        return False, "El código de destino debe ser un código IATA de 3 letras (ej: CTG)."
    if origen == destino:
        return False, "El origen y el destino no pueden ser iguales."
    try:
        datetime.strptime(mes, "%Y-%m")
    except ValueError:
        return False, "El mes debe tener el formato YYYY-MM (ej: 2026-05)."
    return True, ""


def start_gui():
    """Construye la ventana y gestiona todos los eventos de la aplicación."""
    sg.theme(THEME)
    sg.set_options(font=FONT_NORMAL)

    layout = [
        _banner_demo(),
        [sg.Text("Buscador de Vuelos Baratos", font=FONT_TITLE, expand_x=True, justification="center")],
        [sg.HSeparator()],
        [
            sg.Text("Origen (IATA):"), sg.Input(default_text="CLO", key="-ORIGEN-", size=(6, 1)),
            sg.Text("  Destino (IATA):"), sg.Input(default_text="CTG", key="-DESTINO-", size=(6, 1)),
            sg.Text("  Mes (YYYY-MM):"), sg.Input(default_text="2026-05", key="-MES-", size=(9, 1)),
        ],
        [
            sg.Radio("Solo ida", "modo", default=True, key="-SOLO_IDA-"),
            sg.Radio("Ida y vuelta (11–15 días)", "modo", key="-IDA_VUELTA-"),
        ],
        [sg.Button("🔍 Buscar", key="-BUSCAR-", button_color=("white", "#1565C0")),
         sg.Button("📤 Exportar CSV", key="-EXPORTAR-", disabled=True),
         sg.Button("🗑️ Limpiar caché", key="-LIMPIAR-"),
         sg.Exit("❌ Salir")],
        [sg.Table(
            values=[],
            headings=HEADINGS,
            col_widths=COL_ANCHO,
            key="-TABLA-",
            auto_size_columns=False,
            justification="left",
            expand_x=True,
            expand_y=True,
            num_rows=20,
            enable_click_events=True,
            alternating_row_color="#EBF5FB",
            selected_row_colors=("white", "#1565C0"),
        )],
        [sg.StatusBar("Listo.", key="-STATUS-", size=(60, 1), expand_x=True)],
    ]

    window = sg.Window(
        "Buscador de Vuelos Baratos",
        layout,
        resizable=True,
        finalize=True,
        size=(900, 600),
    )

    # Aquí guardamos los resultados actuales para mostrar, exportar y abrir enlaces.
    vuelos_data = []

    while True:
        event, values = window.read()

        if event in (sg.WIN_CLOSED, "❌ Salir"):
            break

        # ── Buscar vuelos ────────────────────────────────────────────────────
        if event == "-BUSCAR-":
            # Leemos y normalizamos entradas del formulario.
            origen = values["-ORIGEN-"].strip().upper()
            destino = values["-DESTINO-"].strip().upper()
            mes = values["-MES-"].strip()
            modo_vuelta = values["-IDA_VUELTA-"]

            valido, msg_error = _validar_inputs(origen, destino, mes)
            if not valido:
                sg.popup_error(msg_error, title="Error de entrada")
                continue

            window["-STATUS-"].update("Buscando vuelos...")
            window["-BUSCAR-"].update(disabled=True)
            window.refresh()

            vuelos_data = []
            fechas = generar_fechas_mes(mes)

            # Recorremos todo el mes para comparar precios y quedarnos con opciones baratas.
            for salida in fechas:
                if modo_vuelta:
                    for dias_retorno in range(11, 16):
                        vuelta = sumar_dias(salida, dias_retorno)
                        cache = cargar_cache(origen, destino, salida, vuelta)
                        if cache:
                            vuelos = cache
                        else:
                            vuelos = buscar_vuelos(origen, destino, salida, vuelta)
                            guardar_cache(origen, destino, salida, vuelta, vuelos)
                        if vuelos:
                            vuelos_data.append(min(vuelos, key=lambda x: x["precio"]))
                else:
                    cache = cargar_cache(origen, destino, salida, None)
                    if cache:
                        vuelos = cache
                    else:
                        vuelos = buscar_vuelos(origen, destino, salida)
                        guardar_cache(origen, destino, salida, None, vuelos)
                    if vuelos:
                        vuelos_data.append(min(vuelos, key=lambda x: x["precio"]))

            vuelos_data = sorted(vuelos_data, key=lambda x: x["precio"])

            # Adaptamos los datos a la estructura esperada por la tabla visual.
            tabla_rows = [
                [
                    v["aerolinea"],
                    formatear_precio_cop(v["precio"]),
                    v["salida"],
                    v.get("vuelta") or "—",
                    v.get("enlace", ""),
                ]
                for v in vuelos_data
            ]
            window["-TABLA-"].update(values=tabla_rows)

            if vuelos_data:
                barato = vuelos_data[0]
                precio_fmt = formatear_precio_cop(barato["precio"])
                window["-STATUS-"].update(
                    f"✈️ Mejor precio: {barato['aerolinea']} — {precio_fmt} | "
                    f"Salida: {barato['salida']}  Vuelta: {barato.get('vuelta') or '—'}  "
                    f"| {len(vuelos_data)} resultado(s) encontrado(s)."
                )
                window["-EXPORTAR-"].update(disabled=False)
            else:
                window["-STATUS-"].update("Sin resultados para el mes indicado.")

            window["-BUSCAR-"].update(disabled=False)

        # ── Exportar CSV ─────────────────────────────────────────────────────
        if event == "-EXPORTAR-" and vuelos_data:
            # Exportamos el resultado exacto que ve el usuario.
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            nombre_archivo = f"vuelos_{timestamp}.csv"
            df = pd.DataFrame(vuelos_data)
            df.to_csv(nombre_archivo, index=False, encoding="utf-8-sig")
            sg.popup(f"Resultados exportados correctamente a:\n{nombre_archivo}", title="Exportación exitosa")

        # ── Limpiar caché ────────────────────────────────────────────────────
        if event == "-LIMPIAR-":
            import sqlite3
            from cache import DB_PATH
            if sg.popup_yes_no("¿Deseas borrar toda la caché de búsquedas guardadas?", title="Confirmar") == "Yes":
                with sqlite3.connect(DB_PATH) as conn:
                    conn.execute("DELETE FROM cache")
                    conn.commit()
                window["-STATUS-"].update("Caché eliminada correctamente.")

        # ── Clic en fila de la tabla → abrir enlace ──────────────────────────
        if isinstance(event, tuple) and event[0] == "-TABLA-" and event[2][0] is not None:
            fila = event[2][0]
            if 0 <= fila < len(vuelos_data):
                enlace = vuelos_data[fila].get("enlace", "")
                if enlace:
                    import webbrowser
                    webbrowser.open(enlace)

    window.close()
