from VehiculoSegmento import VehiculoSegmento


def cargar_escenario(simulador, tipo_escenario):
    """
    Inyecta la cantidad de vehículos correspondiente al escenario seleccionado,
    distribuyendo los VE y PHEV totales entre los modelos de la muestra de control.
    """
    if tipo_escenario == 'Conservador':
        # Total: 9 VE, 3 PHEV
        simulador.agregar_segmento(
            VehiculoSegmento('BYD King (PHEV)',
                             24.57,
                             0.120,
                             3.3,
                             3,
                             'Privado'))
        simulador.agregar_segmento(
            VehiculoSegmento('BYD Dolphin Mini',
                             34.04,
                             0.105,
                             6.6,
                             2,
                             'Privado'))
        simulador.agregar_segmento(
            VehiculoSegmento('Tesla Model Y',
                             69.50,
                             0.146,
                             11.0,
                             2,
                             'Privado'))
        simulador.agregar_segmento(
            VehiculoSegmento('JAC E10X',
                             31.40,
                             0.105,
                             6.6,
                             2,
                             'Privado'))
        simulador.agregar_segmento(
            VehiculoSegmento('Volvo EX30',
                             60.00,
                             0.160,
                             11.0,
                             1,
                             'Privado'))
        simulador.agregar_segmento(
            VehiculoSegmento('MG4 Electric',
                             64.00,
                             0.150,
                             11.0,
                             1,
                             'Privado'))
        simulador.agregar_segmento(
            VehiculoSegmento('Geely EX5 EV',
                             60.22,
                             0.145,
                             11.0,
                             1,
                             'Privado'))

    elif tipo_escenario == 'Tendencial':
        # Total: 11 VE, 3 PHEV
        simulador.agregar_segmento(
            VehiculoSegmento('BYD King (PHEV)',
                             24.57,
                             0.120,
                             3.3,
                             3,
                             'Privado'))
        simulador.agregar_segmento(
            VehiculoSegmento('BYD Dolphin Mini',
                             34.04,
                             0.105,
                             6.6,
                             3,
                             'Privado'))
        simulador.agregar_segmento(
            VehiculoSegmento('Tesla Model Y',
                             69.50,
                             0.146,
                             11.0,
                             2,
                             'Privado'))
        simulador.agregar_segmento(
            VehiculoSegmento('JAC E10X',
                             31.40,
                             0.105,
                             6.6,
                             2,
                             'Privado'))
        simulador.agregar_segmento(
            VehiculoSegmento('Volvo EX30',
                             60.00,
                             0.160,
                             11.0,
                             2,
                             'Privado'))
        simulador.agregar_segmento(
            VehiculoSegmento('MG4 Electric',
                             64.00,
                             0.150,
                             11.0,
                             1,
                             'Privado'))
        simulador.agregar_segmento(
            VehiculoSegmento('Geely EX5 EV',
                             60.22,
                             0.145,
                             11.0,
                             1,
                             'Privado'))

    elif tipo_escenario == 'Acelerado':
        # Total: 14 VE, 4 PHEV
        simulador.agregar_segmento(
            VehiculoSegmento('BYD King (PHEV)',
                             24.57,
                             0.120,
                             3.3,
                             4,
                             'Privado'))
        simulador.agregar_segmento(
            VehiculoSegmento('BYD Dolphin Mini',
                             34.04,
                             0.105,
                             6.6,
                             4,
                             'Privado'))
        simulador.agregar_segmento(
            VehiculoSegmento('Tesla Model Y',
                             69.50,
                             0.146,
                             11.0,
                             3,
                             'Privado'))
        simulador.agregar_segmento(
            VehiculoSegmento('JAC E10X',
                             31.40,
                             0.105,
                             6.6,
                             3,
                             'Privado'))
        simulador.agregar_segmento(
            VehiculoSegmento('Volvo EX30',
                             60.00,
                             0.160,
                             11.0,
                             2,
                             'Privado'))
        simulador.agregar_segmento(
            VehiculoSegmento('MG4 Electric',
                             64.00,
                             0.150,
                             11.0,
                             1,
                             'Privado'))
        simulador.agregar_segmento(
            VehiculoSegmento('Geely EX5 EV',
                             60.22,
                             0.145,
                             11.0,
                             1,
                             'Privado'))

    elif tipo_escenario == 'Sensibilidad':
        # Volumen arbitrario superior para estresar el transformador (Ej. 30 VE, 10 PHEV)
        simulador.agregar_segmento(
            VehiculoSegmento('BYD King (PHEV)',
                             24.57,
                             0.120,
                             3.3,
                             10,
                             'Privado'))
        simulador.agregar_segmento(
            VehiculoSegmento('BYD Dolphin Mini',
                             34.04,
                             0.105,
                             6.6,
                             8,
                             'Privado'))
        simulador.agregar_segmento(
            VehiculoSegmento('Tesla Model Y',
                             69.50,
                             0.146,
                             11.0,
                             6,
                             'Privado'))
        simulador.agregar_segmento(
            VehiculoSegmento('JAC E10X',
                             31.40,
                             0.105,
                             6.6,
                             6,
                             'Privado'))
        simulador.agregar_segmento(
            VehiculoSegmento('Volvo EX30',
                             60.00,
                             0.160,
                             11.0,
                             4,
                             'Privado'))
        simulador.agregar_segmento(
            VehiculoSegmento('MG4 Electric',
                             64.00,
                             0.150,
                             11.0,
                             3,
                             'Privado'))
        simulador.agregar_segmento(
            VehiculoSegmento('Geely EX5 EV',
                             60.22,
                             0.145,
                             11.0,
                             3,
                             'Privado'))

    elif tipo_escenario == 'Example':
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

    else:
        raise ValueError(
            "Escenario no reconocido. Use: 'Conservador', 'Tendencial', 'Acelerado', 'Sensibilidad' o 'Example'.")
