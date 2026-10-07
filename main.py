import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# 1. PARAMETRIZACIÓN BASE Y RESOLUCIÓN TEMPORAL
DIAS_SIMULACION = 30
INTERVALOS_POR_HORA = 12  # Resolución de 5 minutos según metodología IEA
INTERVALOS_POR_DIA = 24 * INTERVALOS_POR_HORA
TOTAL_INTERVALOS = DIAS_SIMULACION * INTERVALOS_POR_DIA
EFICIENCIA_AC = 0.92
LIMITE_DESCARGA = 0.90  # El SOC no baja del 10% (Capacidad neta = 90%)

# Generación del índice de tiempo mensual (Resolución 5 min)
rango_tiempo = pd.date_range(start="2024-01-01 00:00",
                             periods=TOTAL_INTERVALOS, freq="5min")

# Base de datos de la flota
# Formato: [Capacidad_kWh, Consumo_kWh_km, P_real_AC_kW, Cantidad, Perfil_Uso]
flota_ve = {
    'BYD Dolphin Mini': [34.04, 0.105, 6.6, 10, 'Privado'],
    'BYD King (PHEV)': [24.57, 0.120, 3.3, 18, 'Privado'],
    'BYD Yuan Plus': [55.19, 0.125, 7.0, 17, 'Privado'],
    'Chevrolet Equinox EV': [85.00, 0.185, 11.5, 9, 'Privado'],
    'Tesla Model Y': [69.50, 0.146, 11.0, 13, 'Privado'],
    'Tesla Model 3': [69.50, 0.134, 11.0, 8, 'Privado'],
    'JAC E10X': [31.40, 0.105, 6.6, 19, 'Flotilla'],
    'Volvo EX30': [60.00, 0.160, 11.0, 14, 'Privado'],
    'MG4 Electric': [64.00, 0.150, 11.0, 17, 'Privado'],
    'Geely EX5 EV': [60.22, 0.145, 11.0, 8, 'Privado']
}

# Inicialización de la matriz de resultados
resultados_potencia = pd.DataFrame(0.0, index=rango_tiempo,
                                   columns=flota_ve.keys())

# 2. MOTOR DE SIMULACIÓN (MONTECARLO)
np.random.seed(42)

for modelo, parametros in flota_ve.items():
    cap_bat, consumo, p_real_ac, cantidad, perfil = parametros
    cap_neta = cap_bat * LIMITE_DESCARGA

    for unidad in range(cantidad):
        energia_pendiente = 0.0  # Energía acumulada en el vehículo sin cargar

        for dia in range(DIAS_SIMULACION):
            # A) Generación de distancia diaria (Log-normal para privados, Normal para flotillas)
            if perfil == 'Privado':
                # Parámetros para media ~30 km y cola asimétrica de viajes largos
                distancia_dia = np.random.lognormal(mean=3.3, sigma=0.5)
            else:
                # Flotillas con recorridos más estructurados y predecibles
                distancia_dia = np.random.normal(loc=50.0, scale=15.0)

            distancia_dia = max(0, distancia_dia)
            energia_consumida = distancia_dia * consumo
            energia_pendiente += energia_consumida

            # Limitar la energía pendiente a la capacidad máxima extraíble físicamente
            energia_pendiente = min(energia_pendiente, cap_neta)
            soc_actual = (cap_bat - energia_pendiente) / cap_bat

            # B) Decisión estocástica de conexión (Shifting)
            cargar_hoy = True
            if soc_actual > 0.50:
                # Si hay más del 50% de batería, hay un 60% de probabilidad de posponer la carga
                if np.random.random() < 0.60:
                    cargar_hoy = False

            # C) Evento de Carga (Unmanaged Charging - Máxima Potencia)
            if cargar_hoy and energia_pendiente > 0:
                # Hora de llegada al Hogar/Depósito (Media 19:00 hrs)
                hora_llegada = np.random.normal(loc=19.0, scale=2.5)
                hora_llegada = np.clip(hora_llegada, 0, 23.99)

                intervalo_llegada_dia = int(
                    hora_llegada * INTERVALOS_POR_HORA)
                indice_global_inicio = (
                                                   dia * INTERVALOS_POR_DIA) + intervalo_llegada_dia

                potencia_red = p_real_ac / EFICIENCIA_AC
                horas_necesarias = energia_pendiente / (
                            p_real_ac * EFICIENCIA_AC)
                intervalos_necesarios = int(
                    np.ceil(horas_necesarias * INTERVALOS_POR_HORA))

                # Inyección de carga a máxima capacidad desde el momento de conexión
                for i in range(intervalos_necesarios):
                    indice_actual = indice_global_inicio + i
                    if indice_actual < TOTAL_INTERVALOS:
                        # Para el último intervalo, ajustar potencia si requiere una fracción
                        if i == intervalos_necesarios - 1:
                            fraccion = (
                                                   horas_necesarias * INTERVALOS_POR_HORA) - int(
                                horas_necesarias * INTERVALOS_POR_HORA)
                            if fraccion > 0:
                                resultados_potencia.iloc[
                                    indice_actual, resultados_potencia.columns.get_loc(
                                        modelo)] += (potencia_red * fraccion)
                            else:
                                resultados_potencia.iloc[
                                    indice_actual, resultados_potencia.columns.get_loc(
                                        modelo)] += potencia_red
                        else:
                            resultados_potencia.iloc[
                                indice_actual, resultados_potencia.columns.get_loc(
                                    modelo)] += potencia_red

                # Reinicio del acumulador de energía tras la sesión de carga completa
                energia_pendiente = 0.0

# 3. VISUALIZACIÓN DE RESULTADOS
plt.figure(figsize=(16, 7))

plt.stackplot(resultados_potencia.index,
              [resultados_potencia[col] for col in
               resultados_potencia.columns],
              labels=resultados_potencia.columns,
              alpha=0.8)

plt.title(
    'Simulación Montecarlo (Unmanaged Charging): Perfil de Carga AC en Hogar/Depósito (Resolución 5 min)',
    fontsize=14)
plt.ylabel('Demanda Agregada de Potencia Máxima (kW)', fontsize=12)
plt.xlabel('Tiempo (Mes simulado)', fontsize=12)
plt.legend(loc='upper left', bbox_to_anchor=(1.02, 1),
           title="Segmento de Vehículo")
plt.grid(True, alpha=0.3)
plt.tight_layout()

plt.show()