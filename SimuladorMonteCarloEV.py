import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from VehiculoSegmento import VehiculoSegmento

class SimuladorMonteCarloEV:
    """
    Motor de simulación que gestiona el tiempo, agrega la demanda de múltiples
    segmentos de vehículos y extrae estadísticas del sistema.
    """
    def __init__(self, dias=30, resolucion_minutos=5,
                 fecha_inicio="2024-01-01 00:00"):
        self.dias = dias
        self.resolucion_minutos = resolucion_minutos
        self.intervalos_por_hora = 60 // resolucion_minutos
        self.intervalos_por_dia = 24 * self.intervalos_por_hora
        self.total_intervalos = self.dias * self.intervalos_por_dia
        self.fecha_inicio = fecha_inicio

        self.segmentos = []
        self.resultados_df = None
        self.demanda_total = None

    def agregar_segmento(self, segmento: VehiculoSegmento):
        self.segmentos.append(segmento)

    def ejecutar(self):
        """Itera sobre la flota y consolida la matriz de potencia temporal."""
        # np.random.seed(42) # Agregar en caso de requerir un solo resultado siempre
        rango_tiempo = pd.date_range(start=self.fecha_inicio,
                                     periods=self.total_intervalos,
                                     freq=f"{self.resolucion_minutos}min")
        self.resultados_df = pd.DataFrame(index=rango_tiempo)

        for segmento in self.segmentos:
            potencia_agregada_segmento = np.zeros(self.total_intervalos)

            for _ in range(segmento.cantidad):
                potencia_agregada_segmento += segmento.simular_unidad(
                    self.dias, self.intervalos_por_dia,
                    self.intervalos_por_hora
                )

            self.resultados_df[segmento.nombre] = potencia_agregada_segmento

        self.demanda_total = self.resultados_df.sum(axis=1)

    def imprimir_reporte(self):
        """Calcula y muestra los estadísticos críticos de la red eléctrica."""
        demanda_maxima: float
        demanda_promedio: float
        demanda_minima: float
        factor_carga: float
        energia_total_kwh: float

        if self.demanda_total is None:
            raise ValueError(
                "Se debe ejecutar la simulación antes de generar el reporte.")

        demanda_maxima = self.demanda_total.max()
        demanda_promedio = self.demanda_total.mean()
        demanda_minima = self.demanda_total.min()
        energia_total_kwh = self.demanda_total.sum() / self.intervalos_por_hora
        factor_carga = (demanda_promedio / demanda_maxima) * 100 if demanda_maxima > 0 else 0

        print("=" * 45)
        print(" RESUMEN DE SIMULACIÓN MENSUAL ")
        print("=" * 45)
        print(f"Demanda Máxima Coincidente: {demanda_maxima:.2f} kW")
        print(f"Demanda Promedio:           {demanda_promedio:.2f} kW")
        print(f"Demanda Mínima (Valle):     {demanda_minima:.2f} kW")
        print(f"Factor de Carga del Sistema:{factor_carga:.2f} %")
        print(f"Energía Total Demandada:    {energia_total_kwh:,.2f} kWh")
        print("=" * 45)

        return demanda_maxima, demanda_promedio, factor_carga, energia_total_kwh

    def graficar_perfil(self, titulo_grafico: str):
        """Genera la visualización del perfil de carga apilado."""
        max_kw: float
        prom_kw: float
        factor: float
        energia: float

        if self.resultados_df is None:
            raise ValueError(
                "Se debe ejecutar la simulación antes de graficar.")

        max_kw, prom_kw, factor, energia = self.imprimir_reporte()

        plt.figure(figsize=(16, 8))
        plt.stackplot(self.resultados_df.index,
                      [self.resultados_df[col] for col in
                       self.resultados_df.columns],
                      labels=self.resultados_df.columns,
                      alpha=0.8)

        texto_resumen = (f"Demanda Max: {max_kw:.1f} kW | "
                         f"Demanda Prom: {prom_kw:.1f} kW | "
                         f"Factor Carga: {factor:.1f}% | "
                         f"Energía Mensual: {energia / 1000:.2f} MWh")

        plt.title(
            'Perfil de Carga - ' + titulo_grafico,
            fontsize=14, pad=25)
        plt.suptitle(texto_resumen, fontsize=11, color='dimgrey', y=0.91)

        plt.ylabel('Demanda de Potencia (kW)', fontsize=12)
        plt.xlabel('Tiempo (Mes simulado)', fontsize=12)
        plt.legend(loc='upper left', bbox_to_anchor=(1.02, 1),
                   title="Segmentos")
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        plt.show()
