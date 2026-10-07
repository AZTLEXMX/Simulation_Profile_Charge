import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# 1. PARAMETRIZACIÓN BASE
DIAS_SIMULACION = 30
INTERVALOS_POR_HORA = 4  # Resolución de 15 minutos
INTERVALOS_POR_DIA = 24 * INTERVALOS_POR_HORA
TOTAL_INTERVALOS = DIAS_SIMULACION * INTERVALOS_POR_DIA
EFICIENCIA_AC = 0.92

# Generación del índice de tiempo mensual (Mes genérico de 30 días)
rango_tiempo = pd.date_range(start="2024-01-01 00:00",
                             periods=TOTAL_INTERVALOS, freq="15min")

# Base de datos de la flota (Extraída de la matriz de Excel)
# Formato: 'Modelo': [Capacidad_kWh, Consumo_kWh_km, P_real_AC_kW, Cantidad_Flota]
flota_ve = {
    'BYD Dolphin Mini': [34.04, 0.105, 6.6, 10],
    'BYD King (PHEV)': [24.57, 0.120, 3.3, 18],
    'BYD Yuan Plus': [55.19, 0.125, 7.0, 17],
    'Chevrolet Equinox EV': [85.00, 0.185, 11.5, 9],
    'Tesla Model Y': [69.50, 0.146, 11.0, 13],
    'Tesla Model 3': [69.50, 0.134, 11.0, 8],
    'JAC E10X': [31.40, 0.105, 6.6, 19],
    'Volvo EX30': [60.00, 0.160, 11.0, 14],
    'MG4 Electric': [64.00, 0.150, 11.0, 17],
    'Geely EX5 EV': [60.22, 0.145, 11.0, 8]
}

# Inicialización de la matriz de resultados (Potencia agregada por modelo y por intervalo)
resultados_potencia = pd.DataFrame(0.0, index=rango_tiempo,
                                   columns=flota_ve.keys())

# 2. MOTOR DE SIMULACIÓN (MONTECARLO)
np.random.seed(42)  # Semilla para reproducibilidad de resultados

for modelo, parametros in flota_ve.items():
    cap_bat, consumo, p_real_ac, cantidad = parametros

    for unidad in range(cantidad):
        # Simulación día por día para cada vehículo individual
        for dia in range(DIAS_SIMULACION):

            # Paso A: Generación aleatoria de distancia recorrida diaria
            # Media de 30 km diarios, desviación estándar de 10 km
            distancia_dia = np.random.normal(loc=30.0, scale=10.0)
            distancia_dia = max(0,
                                distancia_dia)  # Evitar distancias negativas

            energia_consumida = distancia_dia * consumo
            energia_a_reponer = min(energia_consumida,
                                    cap_bat)  # No exceder capacidad física

            # Paso B: Decisión de carga (Simplificada: asume carga diaria si se usó el vehículo)
            if energia_a_reponer > 1.0:  # Umbral mínimo para iniciar carga

                # Paso C: Hora de llegada estocástica
                # Media 19:00 h (19.0), desviación estándar de 2 horas
                hora_llegada = np.random.normal(loc=19.0, scale=2.0)
                hora_llegada = np.clip(hora_llegada, 0,
                                       23.99)  # Acotar a formato 24h

                # Convertir hora de llegada al índice del intervalo del día correspondiente
                intervalo_llegada_dia = int(
                    hora_llegada * INTERVALOS_POR_HORA)
                indice_global_inicio = (
                                                   dia * INTERVALOS_POR_DIA) + intervalo_llegada_dia

                # Paso D: Cálculo de duración y mapeo de potencia
                potencia_red = p_real_ac / EFICIENCIA_AC
                horas_necesarias = energia_a_reponer / (
                            p_real_ac * EFICIENCIA_AC)
                intervalos_necesarios = int(
                    np.ceil(horas_necesarias * INTERVALOS_POR_HORA))

                # Inyección de potencia en la matriz a lo largo del tiempo de carga
                for i in range(intervalos_necesarios):
                    indice_actual = indice_global_inicio + i
                    # Evitar desbordamiento al final del mes
                    if indice_actual < TOTAL_INTERVALOS:
                        resultados_potencia.iloc[
                            indice_actual, resultados_potencia.columns.get_loc(
                                modelo)] += potencia_red

# 3. VISUALIZACIÓN DE RESULTADOS
plt.figure(figsize=(16, 7))

# Configuración del gráfico de áreas apiladas ("Stacked Chart")
plt.stackplot(resultados_potencia.index,
              [resultados_potencia[col] for col in
               resultados_potencia.columns],
              labels=resultados_potencia.columns,
              alpha=0.8)

plt.title(
    'Simulación Montecarlo Mensual: Perfil de Carga de Vehículos Eléctricos en AC',
    fontsize=14)
plt.ylabel('Demanda Agregada de Potencia (kW)', fontsize=12)
plt.xlabel('Tiempo (Mes simulado)', fontsize=12)
plt.legend(loc='upper left', bbox_to_anchor=(1.02, 1),
           title="Segmento de Vehículo")
plt.grid(True, alpha=0.3)
plt.tight_layout()

# Opcional: Acercamiento a una semana específica para replicar la vista de IEA
# plt.xlim(pd.Timestamp('2024-01-08'), pd.Timestamp('2024-01-15'))

plt.show()