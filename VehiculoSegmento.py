import numpy as np

class VehiculoSegmento:
    """
    Representa un segmento de vehículos homogéneos dentro de la flota.
    Encapsula las características físicas y el comportamiento estocástico individual.
    """
    def __init__(self, nombre, cap_bat_kwh, consumo_kwh_km, p_max_ac_kw,
                 cantidad, perfil_uso,
                 limite_descarga=0.90, eficiencia_ac=0.92):
        self.nombre = nombre
        self.cap_bat = cap_bat_kwh
        self.consumo = consumo_kwh_km
        self.p_max_ac = p_max_ac_kw
        self.cantidad = cantidad
        self.perfil_uso = perfil_uso
        self.cap_neta = cap_bat_kwh * limite_descarga
        self.eficiencia_ac = eficiencia_ac

    def _generar_distancia_diaria(self):
        """Genera la distancia recorrida basada en distribuciones estadísticas según el perfil."""
        if self.perfil_uso == 'Privado':
            # Distribución Log-normal: mayoría de viajes cortos, pocos viajes muy largos
            dist = np.random.lognormal(mean=3.3, sigma=0.5)
        else:
            # Distribución Normal: rutas de flotilla más predecibles
            dist = np.random.normal(loc=50.0, scale=15.0)
        return max(0, dist)

    def simular_unidad(self, dias_simulacion, intervalos_por_dia,
                       intervalos_por_hora):
        """
        Ejecuta la simulación mensual para un solo vehículo del segmento.
        Retorna un arreglo NumPy con el perfil de potencia de carga.
        """
        total_intervalos = dias_simulacion * intervalos_por_dia
        perfil_potencia = np.zeros(total_intervalos)
        energia_pendiente = 0.0

        for dia in range(dias_simulacion):
            distancia = self._generar_distancia_diaria()
            energia_consumida = distancia * self.consumo
            energia_pendiente = min(energia_pendiente + energia_consumida,
                                    self.cap_neta)

            soc_actual = (self.cap_bat - energia_pendiente) / self.cap_bat

            # Lógica de Shifting (probabilidad de posponer carga si el SOC > 50%)
            cargar_hoy = True
            if soc_actual > 0.50 and np.random.random() < 0.60:
                cargar_hoy = False

            if cargar_hoy and energia_pendiente > 0:
                # Llegada estocástica (Media 19:00 hrs)
                hora_llegada = np.clip(np.random.normal(loc=19.0, scale=2.5),
                                       0, 23.99)
                indice_inicio = (dia * intervalos_por_dia) + int(
                    hora_llegada * intervalos_por_hora)

                potencia_red = self.p_max_ac / self.eficiencia_ac
                horas_necesarias = energia_pendiente / (
                            self.p_max_ac * self.eficiencia_ac)
                intervalos_necesarios = int(
                    np.ceil(horas_necesarias * intervalos_por_hora))

                for i in range(intervalos_necesarios):
                    idx = indice_inicio + i
                    if idx < total_intervalos:
                        # Ajuste proporcional para el último intervalo de carga
                        if i == intervalos_necesarios - 1:
                            fraccion = (
                                                   horas_necesarias * intervalos_por_hora) - int(
                                horas_necesarias * intervalos_por_hora)
                            perfil_potencia[idx] += (
                                        potencia_red * fraccion) if fraccion > 0 else potencia_red
                        else:
                            perfil_potencia[idx] += potencia_red

                energia_pendiente = 0.0  # Batería al 100% (o 90% neto) tras finalizar

        return perfil_potencia
