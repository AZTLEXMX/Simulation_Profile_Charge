from SimuladorMonteCarloEV import SimuladorMonteCarloEV
from escenarios import cargar_escenario


if __name__ == "__main__":
    # Escenarios disponibles:
    # 'Conservador' | 'Tendencial' | 'Acelerado' | 'Sensibilidad' | 'Example'
    # Definir el escenario a evaluar
    ESCENARIO_ACTUAL = 'Conservador'
    # ESCENARIO_ACTUAL = 'Tendencial'
    # ESCENARIO_ACTUAL = 'Acelerado'
    # ESCENARIO_ACTUAL = 'Sensibilidad'
    # ESCENARIO_ACTUAL = 'Example'

    # Instanciar el entorno de simulación
    simulador = SimuladorMonteCarloEV(dias=30, resolucion_minutos=5)

    # Cargar la configuración de la flota
    cargar_escenario(simulador, ESCENARIO_ACTUAL)

    # Ejecutar el motor estocástico
    simulador.ejecutar()

    # Generar métricas y gráfica
    simulador.graficar_perfil(titulo_grafico=ESCENARIO_ACTUAL)
