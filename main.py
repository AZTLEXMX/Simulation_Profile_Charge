import argparse
from SimuladorMonteCarloEV import SimuladorMonteCarloEV
from escenarios import cargar_escenario, CONFIGURACION_ESCENARIOS


def main():
    parser = argparse.ArgumentParser(
        prog="prelectrics",
        description="Simulador Estocástico de Perfiles de Carga de Vehículos Eléctricos (VE y PHEV)."
    )

    # Argumento obligatorio: Escenario
    parser.add_argument(
        "-e", "--escenario",
        type=str,
        required=True,
        choices=list(CONFIGURACION_ESCENARIOS.keys()),
        help="Escenario de penetración a evaluar."
    )

    # Argumento opcional: Temperatura ambiente
    parser.add_argument(
        "-t", "--temperatura",
        type=float,
        default=16.0,
        help="Temperatura ambiente media en °C, por defecto: 16.0 °C."
    )

    # Argumento opcional: Días simulados
    parser.add_argument(
        "-d", "--dias",
        type=int,
        default=30,
        help="Cantidad de días a simular, por defecto: 30 días."
    )

    args = parser.parse_args()

    # Instanciar el entorno de simulación con los parámetros recibidos de la terminal
    simulador = SimuladorMonteCarloEV(
        dias=args.dias,
        resolucion_minutos=5,
        temperatura_c=args.temperatura
    )

    # Cargar la configuración de la flota
    cargar_escenario(simulador, args.escenario)

    # Ejecutar el motor estocástico
    simulador.ejecutar()

    # Generar métricas y gráfica
    simulador.graficar_perfil(titulo_grafico=args.escenario)


if __name__ == "__main__":
    main()