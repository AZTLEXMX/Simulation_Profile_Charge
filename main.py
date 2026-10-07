from SimuladorMonteCarloEV import SimuladorMonteCarloEV
from VehiculoSegmento import VehiculoSegmento


if __name__ == "__main__":
    # Instanciar el entorno de simulación
    simulador = SimuladorMonteCarloEV(dias=30, resolucion_minutos=5)

    # Agregar segmentos de manera interactiva e independiente
    simulador.agregar_segmento(
        VehiculoSegmento('BYD Dolphin Mini',
                         34.04,
                         0.105,
                         6.6,
                         10,
                         'Privado'))
    simulador.agregar_segmento(
        VehiculoSegmento('BYD King (PHEV)',
                         24.57,
                         0.120,
                         3.3,
                         18,
                         'Privado'))
    simulador.agregar_segmento(
        VehiculoSegmento('BYD Yuan Plus',
                         55.19,
                         0.125,
                         7.0,
                         17,
                         'Privado'))
    simulador.agregar_segmento(
        VehiculoSegmento('Chevrolet Equinox EV',
                         85.00,
                         0.185,
                         11.5,
                         9,
                         'Privado'))
    simulador.agregar_segmento(
        VehiculoSegmento('Tesla Model Y',
                         69.50,
                         0.146,
                         11.0,
                         13,
                         'Privado'))
    simulador.agregar_segmento(
        VehiculoSegmento('Tesla Model 3',
                         69.50,
                         0.134,
                         11.0,
                         8,
                         'Privado'))
    simulador.agregar_segmento(
        VehiculoSegmento('JAC E10X',
                         31.40,
                         0.105,
                         6.6,
                         19,
                         'Flotilla'))
    simulador.agregar_segmento(
        VehiculoSegmento('Volvo EX30',
                         60.00,
                         0.160,
                         11.0,
                         14,
                         'Privado'))
    simulador.agregar_segmento(
        VehiculoSegmento('MG4 Electric',
                         64.00,
                         0.150,
                         11.0,
                         17,
                         'Privado'))
    simulador.agregar_segmento(
        VehiculoSegmento('Geely EX5 EV',
                         60.22,
                         0.145,
                         11.0,
                         8,
                         'Privado'))

    # Ejecutar motor estocástico
    simulador.ejecutar()

    # Consolidar métricas y generar gráfica
    simulador.graficar_perfil()