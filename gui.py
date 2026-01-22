import PySimpleGUI as sg
import pandas as pd
from api import buscar_vuelos, generar_fechas_mes
from utils import sumar_dias
from cache import guardar_cache, cargar_cache


def start_gui():
    sg.theme("LightBlue")

    layout = [
        [sg.Text("Origen:"), sg.Input(default_text="CLO", key="-ORIGEN-", size=(6,1)),
         sg.Text("Destino:"), sg.Input(default_text="CTG", key="-DESTINO-", size=(6,1))],
        [sg.Text("Mes (YYYY-MM):"), sg.Input(default_text="2026-05", key="-MES-", size=(8,1))],
        [sg.Radio("Solo ida", "modo", default=True, key="-SOLO_IDA-"),
         sg.Radio("Ida y vuelta", "modo", key="-IDA_VUELTA-")],
        [sg.Button("Buscar", key="-BUSCAR-")],
        [sg.Table(values=[], headings=["Aerolínea","Precio","Salida","Vuelta","Enlace"],
                  key="-TABLA-", auto_size_columns=True, justification='left',
                  expand_x=True, expand_y=True, num_rows=20)],
        [sg.Button("Exportar CSV", key="-EXPORTAR-"), sg.Exit()]
    ]

    window = sg.Window("Buscador de Vuelos Baratos", layout, resizable=True)
    vuelos_data = []

    while True:
        event, values = window.read()
        if event in (sg.WIN_CLOSED, "Exit"):
            break

        if event == "-BUSCAR-":
            origen = values["-ORIGEN-"].strip().upper()
            destino = values["-DESTINO-"].strip().upper()
            mes = values["-MES-"]
            modo_vuelta = values["-IDA_VUELTA-"]

            vuelos_data = []
            fechas = generar_fechas_mes(mes)

            for salida in fechas:
                if modo_vuelta:
                    # Modo ida y vuelta
                    for dias_retorno in [11, 12, 13, 14, 15]:
                        vuelta = sumar_dias(salida, dias_retorno)
                        cache = cargar_cache(origen, destino, salida, vuelta)
                        if cache:
                            vuelos = cache
                        else:
                            vuelos = buscar_vuelos(origen, destino, salida, vuelta)
                            guardar_cache(origen, destino, salida, vuelta, vuelos)

                        # Tomar solo el vuelo más barato del conjunto
                        if vuelos:
                            vuelo = min(vuelos, key=lambda x: x["precio"])
                            vuelos_data.append(vuelo)
                else:
                    # Solo ida
                    cache = cargar_cache(origen, destino, salida, None)
                    if cache:
                        vuelos = cache
                    else:
                        vuelos = buscar_vuelos(origen, destino, salida)
                        guardar_cache(origen, destino, salida, None, vuelos)
                    if vuelos:
                        vuelo = min(vuelos, key=lambda x: x["precio"])
                        vuelos_data.append(vuelo)

            # Ordenar por precio total
            vuelos_data = sorted(vuelos_data, key=lambda x: x["precio"])

            # Mostrar resultados
            df = pd.DataFrame(vuelos_data)
            window["-TABLA-"].update(values=df.values.tolist())

            if vuelos_data:
                barato = vuelos_data[0]
                sg.popup(f"✈️ El vuelo más barato es de {barato['aerolinea']} "
                         f"por ${barato['precio']} (ida: {barato['salida']} - vuelta: {barato.get('vuelta', '—')}).")

        if event == "-EXPORTAR-" and vuelos_data:
            df = pd.DataFrame(vuelos_data)
            df.to_csv("vuelos_resultados.csv", index=False)
            sg.popup("Resultados exportados a vuelos_resultados.csv")

    window.close()
