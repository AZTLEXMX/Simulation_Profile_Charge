from dataclasses import dataclass
from VehiculoSegmento import VehiculoSegmento


@dataclass(frozen=True)
class FichaTecnicaVE:
    """Estructura inmutable que almacena las especificaciones físicas únicas de cada vehículo."""
    nombre: str
    cap_bat_kwh: float
    consumo_kwh_km: float
    p_max_ac_kw: float
    perfil_defecto: str = 'Privado'


class CatalogoVehiculos:
    """
    Catálogo centralizado (Patrón Factory) que define los vehículos una sola vez
    y genera instancias de VehiculoSegmento bajo demanda.
    """
    _MODELOS = {
        'BYD_KING': FichaTecnicaVE('BYD King (PHEV)', 24.57, 0.120, 3.3),
        'DOLPHIN_MINI': FichaTecnicaVE('BYD Dolphin Mini', 34.04, 0.105, 6.6),
        'MODEL_Y': FichaTecnicaVE('Tesla Model Y', 69.50, 0.146, 11.0),
        'MODEL_3': FichaTecnicaVE('Tesla Model 3', 69.50, 0.134, 11.0),
        'JAC_E10X': FichaTecnicaVE('JAC E10X', 31.40, 0.105, 6.6),
        'VOLVO_EX30': FichaTecnicaVE('Volvo EX30', 60.00, 0.160, 11.0),
        'MG4': FichaTecnicaVE('MG4 Electric', 64.00, 0.150, 11.0),
        'YUAN_PLUS': FichaTecnicaVE('BYD Yuan Plus', 55.19, 0.125, 7.0),
        'EQUINOX_EV': FichaTecnicaVE('Chevrolet Equinox EV', 85.00, 0.185, 11.5),
        'GEELY_EX5': FichaTecnicaVE('Geely EX5 EV', 60.22, 0.145, 11.0),
    }

    @classmethod
    def crear_segmento(cls, clave_modelo: str, cantidad: int, perfil_uso: str = None, **kwargs) -> VehiculoSegmento:
        """
        Instancia un VehiculoSegmento combinando la ficha técnica base con la cantidad del escenario.
        Permite sobrescribir el perfil_uso o pasar parámetros extra (como distancia_media).
        """
        if clave_modelo not in cls._MODELOS:
            raise KeyError(f"El modelo '{clave_modelo}' no existe en el catálogo.")

        ficha = cls._MODELOS[clave_modelo]
        perfil_final = perfil_uso if perfil_uso is not None else ficha.perfil_defecto

        return VehiculoSegmento(
            nombre=ficha.nombre,
            cap_bat_kwh=ficha.cap_bat_kwh,
            consumo_kwh_km=ficha.consumo_kwh_km,
            p_max_ac_kw=ficha.p_max_ac_kw,
            cantidad=cantidad,
            perfil_uso=perfil_final,
            **kwargs
        )


# Matriz de configuración de escenarios: Solo define cantidades (o tuplas si cambia el perfil de uso)
CONFIGURACION_ESCENARIOS = {
    'Conservador': {  # Total: 9 VE, 3 PHEV
        'BYD_KING': 3,
        'DOLPHIN_MINI': 1,
        'MODEL_Y': 1,
        'MODEL_3': 1,
        'JAC_E10X': 1,
        'VOLVO_EX30': 1,
        'MG4': 1,
        'YUAN_PLUS': 1,
        'EQUINOX_EV': 1,
        'GEELY_EX5': 1,
    },
    'Tendencial': {  # Total: 11 VE, 3 PHEV
        'BYD_KING': 3,
        'DOLPHIN_MINI': 1,
        'MODEL_Y': 1,
        'MODEL_3': 2,
        'JAC_E10X': 1,
        'VOLVO_EX30': 1,
        'MG4': 1,
        'YUAN_PLUS': 2,
        'EQUINOX_EV': 1,
        'GEELY_EX5': 1,
    },
    'Acelerado': {  # Total: 14 VE, 4 PHEV
        'BYD_KING': 4,
        'DOLPHIN_MINI': 3,
        'MODEL_Y': 1,
        'MODEL_3': 1,
        'JAC_E10X': 2,
        'VOLVO_EX30': 2,
        'MG4': 1,
        'YUAN_PLUS': 2,
        'EQUINOX_EV': 1,
        'GEELY_EX5': 1,
    },
    'Sensibilidad': {  # Total: 35 VE, 10 PHEV
        'BYD_KING': 10,
        'DOLPHIN_MINI': 8,
        'MODEL_Y': 5,
        'MODEL_3': 4,
        'JAC_E10X': 2,
        'VOLVO_EX30': 4,
        'MG4': 2,
        'YUAN_PLUS': 4,
        'EQUINOX_EV': 4,
        'GEELY_EX5': 2,
    },
    'Example': {
        'DOLPHIN_MINI': 10,
        'BYD_KING': 18,
        'YUAN_PLUS': 17,
        'EQUINOX_EV': 9,
        'MODEL_Y': 13,
        'MODEL_3': 8,
        'JAC_E10X': (19, 'Flotilla'),  # Caso especial que sobrescribe el perfil 'Privado' a 'Flotilla'
        'VOLVO_EX30': 14,
        'MG4': 17,
        'GEELY_EX5': 8,
    }
}


def cargar_escenario(simulador, tipo_escenario: str):
    """
    Inyecta la cantidad de vehículos correspondiente al escenario seleccionado
    consultando el catálogo centralizado.
    """
    if tipo_escenario not in CONFIGURACION_ESCENARIOS:
        opciones = ", ".join([f"'{k}'" for k in CONFIGURACION_ESCENARIOS.keys()])
        raise ValueError(f"Escenario no reconocido. Use: {opciones}.")

    distribucion = CONFIGURACION_ESCENARIOS[tipo_escenario]

    for clave_modelo, config in distribucion.items():
        # Permite manejar tanto un entero simple (cantidad) como una tupla (cantidad, perfil_uso)
        if isinstance(config, tuple):
            cantidad, perfil = config
            segmento = CatalogoVehiculos.crear_segmento(clave_modelo, cantidad, perfil_uso=perfil)
        else:
            segmento = CatalogoVehiculos.crear_segmento(clave_modelo, cantidad=config)

        simulador.agregar_segmento(segmento)