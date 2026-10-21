import numpy as np


class VehiculoSegmento:
    """
    Representa un segmento de vehículos homogéneos dentro de la flota.
    Encapsula las características físicas y el comportamiento estocástico individual.
    """

    def __init__(self, nombre, cap_bat_kwh, consumo_kwh_km, p_max_ac_kw,
                 cantidad, perfil_uso, distancia_media=113.0,
                 distancia_std=28.0,
                 limite_descarga=0.90, eficiencia_ac=0.92):
        self.nombre = nombre
        self.cap_bat = cap_bat_kwh
        self.consumo = consumo_kwh_km
        self.p_max_ac = p_max_ac_kw
        self.cantidad = cantidad
        self.perfil_uso = perfil_uso
        self.distancia_media = distancia_media
        self.distancia_std = distancia_std
        self.cap_neta = cap_bat_kwh * limite_descarga
        self.eficiencia_ac = eficiencia_ac


    def _generar_distancia_diaria(self):
        """Genera la distancia basada en los parámetros dinámicos de entrada."""
        if self.perfil_uso == 'Privado':
            # Conversión de Media y Desviación Estándar a parámetros mu y sigma de Log-normal
            varianza = self.distancia_std ** 2
            sigma_log = np.sqrt(
                np.log((varianza / (self.distancia_media ** 2)) + 1))
            mu_log = np.log(self.distancia_media) - (sigma_log ** 2) / 2
            dist = np.random.lognormal(mean=mu_log, sigma=sigma_log)
        else:
            # Distribución Normal directa para flotillas
            dist = np.random.normal(loc=self.distancia_media,
                                    scale=self.distancia_std)

        return max(0, dist)

    def _calcular_factores_termicos(self, temperatura_c):
        """
        Calcula los factores de ajuste por temperatura ambiente (Metodología IEA).
        Temperatura base ideal: 21.5 °C.
        """
        temp_optima = 21.5
        desviacion = abs(temperatura_c - temp_optima)

        # Penalización en descarga (consumo en ruta):
        # Incrementa ~1.2% por cada °C de frío (<21.5)
        # o ~0.8% por cada °C de calor (>21.5) por uso de A/C
        if temperatura_c < temp_optima:
            factor_consumo = 1.0 + (0.012 * desviacion)
        else:
            factor_consumo = 1.0 + (0.008 * desviacion)

        # Penalización en eficiencia de carga (disipación y BTMS):
        # Reduce la eficiencia ~0.2% por cada °C de desviación respecto a la óptima
        penalizacion_carga = 1.0 - (0.002 * desviacion)
        eficiencia_ajustada = np.clip(self.eficiencia_ac * penalizacion_carga,
                                      0.70, 0.98)

        return self.consumo * factor_consumo, eficiencia_ajustada

    def simular_unidad(self, dias_simulacion, intervalos_por_dia,
                       intervalos_por_hora, temperatura_c=21.5):
        """
        Ejecuta la simulación mensual para un solo vehículo del segmento,
        integrando la afectación térmica en descarga y recarga.
        """
        total_intervalos = dias_simulacion * intervalos_por_dia
        perfil_potencia = np.zeros(total_intervalos)
        energia_pendiente = 0.0

        # Obtener consumo real y eficiencia de carga afectados por la temperatura
        consumo_real, eficiencia_real = self._calcular_factores_termicos(
            temperatura_c)

        for dia in range(dias_simulacion):
            distancia = self._generar_distancia_diaria()
            energia_consumida = distancia * consumo_real
            energia_pendiente = min(energia_pendiente + energia_consumida,
                                    self.cap_neta)
            soc_actual = (self.cap_bat - energia_pendiente) / self.cap_bat

            # Lógica de Shifting (probabilidad de posponer carga si el SOC > 50%)
            cargar_hoy = True
            if soc_actual > 0.50 and np.random.random() < 0.60:
                cargar_hoy = False

            if cargar_hoy and energia_pendiente > 0:
                # Llegada estocástica (Media 20:00 hrs)
                hora_llegada = np.clip(np.random.normal(loc=20.0, scale=2.5),
                                       0, 23.99)
                indice_inicio = (dia * intervalos_por_dia) + int(
                    hora_llegada * intervalos_por_hora)

                # Se utiliza la eficiencia_real ajustada térmicamente
                potencia_red = self.p_max_ac / eficiencia_real
                horas_necesarias = energia_pendiente / (
                            self.p_max_ac * eficiencia_real)
                intervalos_necesarios = int(
                    np.ceil(horas_necesarias * intervalos_por_hora))

                for i in range(intervalos_necesarios):
                    idx = indice_inicio + i
                    if idx < total_intervalos:
                        # Ajuste proporcional para el último intervalo de carga
                        if i == intervalos_necesarios - 1:
                            fraccion = (horas_necesarias * intervalos_por_hora) - int(
                                horas_necesarias * intervalos_por_hora)
                            perfil_potencia[idx] += (
                                        potencia_red * fraccion) if fraccion > 0 else potencia_red
                        else:
                            perfil_potencia[idx] += potencia_red

                energia_pendiente = 0.0  # Batería al 100% (o 90% neto) tras finalizar

        return perfil_potencia
