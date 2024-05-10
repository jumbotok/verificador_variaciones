# Período a validar
primero_de_mes_mas_uno = '2024-05-02'
fecha_fin = '2024-05-09'

print(f"Verificación de variación de precios entre {primero_de_mes_mas_uno} y {fecha_fin}\n")

# variación precios
variacion_precios = {
    # NO HAY PUBLICACION PORQUE ES CERO, se publicará a futuro por dato 1D
    '2024-05-01': { 'variacion_precios': 0.00              , 'variacion_precios_1D': 1.1542629190877136  },
    # https://x.com/Bot_JumboOk/status/1785992611662049548
    '2024-05-02': { 'variacion_precios': 1.1584416530775457, 'variacion_precios_1D': 1.1584416530775457  },
    # https://x.com/Bot_JumboOk/status/1786355086035390491
    '2024-05-03': { 'variacion_precios': 0.5064845706715744, 'variacion_precios_1D': -0.6444910298656623 },
    # https://x.com/Bot_JumboOk/status/1786717290911969678
    '2024-05-04': { 'variacion_precios': 0.4901422687799481, 'variacion_precios_1D': -0.0162599477649934 },
    # https://x.com/Bot_JumboOk/status/1787079722893230249
    '2024-05-05': { 'variacion_precios': 0.1564897189304304, 'variacion_precios_1D': -0.3320251542256756 },
    # https://x.com/Bot_JumboOk/status/1787442348823105626
    '2024-05-06': { 'variacion_precios': 1.3749888309809108, 'variacion_precios_1D': 1.2165952655388992  },
    # https://x.com/Bot_JumboOk/status/1787805133499240675
    '2024-05-07': { 'variacion_precios': 1.1080667911012654, 'variacion_precios_1D': -0.2633016713073601 },
    # https://x.com/Bot_JumboOk/status/1788167556794081325
    '2024-05-08': { 'variacion_precios': 1.074701536116322 , 'variacion_precios_1D': -0.0329995974049097 },
    # https://x.com/Bot_JumboOk/status/1788529517839212748
    '2024-05-09': { 'variacion_precios': 1.512453681518906 , 'variacion_precios_1D': 0.4330976384294871  }
}

def calc_tasa_inflacion_acumuladas(variaciones:dict):
    """
    Calcula tasa de inflación acumuladas usando la variación de precio 1D

    Parámetros:
        variaciones -- dict de variaciones de precios 1D para acumular

    Retorna:
        arreglo de tuplas con fecha e inflación acumulada para un periodo dado
    """

    # Inicializo tasa inflacion acumulada
    tasa_inflacion_acumulada = 0

    # Lista tasa inflacion acumulada
    tasa_inflacion_acumuladas = []

    # Ordena lista por fecha
    variaciones_orden_fecha = sorted(variaciones, key=lambda x: x[0])

    # Calcula tasa de inflación acumuladas
    for fecha, variaciones_fecha in variaciones_orden_fecha:
        tasa_inflacion_acumulada = ((1 + (variaciones_fecha['variacion_precios_1D'] / 100)) * (1 + tasa_inflacion_acumulada)) - 1
        tasa_inflacion_acumuladas.append((fecha, tasa_inflacion_acumulada * 100))

    return tasa_inflacion_acumuladas

def tasa_inflacion_acumladas_por_rango_de_fechas(variaciones, fecha_inicio, fecha_fin):
    """
    Filtra variaciones de precios para un rango de fechas e invoca
    función de cálculo de tasa de inflación acumulada

    Parámetros:
        variaciones  -- dict con variaciones de precios
        fecha_inicio -- str formato ISO 8601
        fecha_fin    -- str formato ISO 8601

    Retorna:
        arreglo de tuplas con fecha e inflación acumulada para un periodo dado
    """

    # Convierte diccionario de variaciones en lista de tuplas y filtra por rango de fecha
    variaciones_para_rango_de_fechas = [(fecha, variaciones_fecha) for fecha, variaciones_fecha in variaciones.items()
                               if fecha_inicio <= fecha <= fecha_fin]

    return calc_tasa_inflacion_acumuladas(variaciones_para_rango_de_fechas)

def verifica_variacion_contra_1D(fecha_verificacion, variacion_precios_para_el_dia, tasa_inflacion_acumulada, tolerancia_error=1e-12):
    """
    Compara variaciones de precios teniendo en cuenta una cierta toleracia de error.
    Imprime por en caso de pasar or fallar la verificación.

    Parámetros:
        fecha_verificacion            -- str formato ISO 8601
        variacion_precios_para_el_dia -- float
        tasa_inflacion_acumulada      -- float
        tolerancia_error              -- float
    """

    if  abs(variacion_precios_para_el_dia - tasa_inflacion_acumulada) < tolerancia_error:
        print(f"[✓] variación precios al {fecha_verificacion} {variacion_precios_para_el_dia} contra tasa inflación acumuladsa 1D {tasa_inflacion_acumulada} con tolerancia {tolerancia_error}")
    else:
        print(f"[𐄂] variación precios al {fecha_verificacion} {variacion_precios_para_el_dia} contra tasa inflación acumuladsa 1D {tasa_inflacion_acumulada} con tolerancia {tolerancia_error}")

def valida_variaciones_de_precios_contra_1D(variacion_precios, fecha_inicio, fecha_fin):
    """
    Validación de lista de variacion de precios contra variación precio 1D

    Parámetros:
        variacion_precios -- dict
        fecha_inicio      -- str formato ISO 8601. Es la fecha contra la que se calcula la variación de precios (ej, inicio de variación mennsual o semanal, etc)
        fecha_fin         -- str formato ISO 8601. Fecha hasta la cual se desea obtner tasa de inflación acumulada
    """
    # Obtiene tasas de inflación acumuladas para todas las fechas
    tasa_inflacion_acumuladas = tasa_inflacion_acumladas_por_rango_de_fechas(variacion_precios, fecha_inicio, fecha_fin)

    # Recorremos cada una de las tasa de inflación acumuladas y verificamos con variación de precio para la misma fecha
    for fecha, tasa_inflacion_acumalada in tasa_inflacion_acumuladas:
        variacion_precios_de_la_fecha = variacion_precios[fecha]['variacion_precios']
        verifica_variacion_contra_1D(fecha, variacion_precios_de_la_fecha, tasa_inflacion_acumalada)

# Validación
valida_variaciones_de_precios_contra_1D(variacion_precios, primero_de_mes_mas_uno, fecha_fin)

print("\n⚇")
