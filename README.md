# Simulador Estocástico de Perfiles de Carga de Vehículos Eléctricos (VE y PHEV)

Este repositorio contiene una herramienta de línea de comandos (CLI) e interfaz de simulación de Montecarlo desarrollada en Python para estimar los perfiles de carga agregados de Vehículos Eléctricos (VE) y Vehículos Híbridos Enchufables (PHEV).

El modelo computacional se fundamenta en los lineamientos técnicos de la Agencia Internacional de Energía (IEA) y emplea Programación Orientada a Objetos (POO) junto con el patrón de diseño *Factory/Catálogo* para garantizar la integridad de los datos y la escalabilidad del código.

## 📂 Estructura del Repositorio

El código está modularizado en cinco archivos principales:

* `pyproject.toml`: Archivo de configuración de empaquetado que gestiona las dependencias y registra el comando ejecutable `prelectrics` en el entorno del sistema.
* `main.py`: Punto de entrada de la aplicación CLI. Procesa los argumentos desde la terminal (`argparse`), inicializa el entorno de simulación y coordina la ejecución y salida gráfica.


* `escenarios.py`: Implementa el catálogo inmutable de vehículos (`FichaTecnicaVE` y `CatalogoVehiculos`) y las matrices de configuración por escenario, evitando la duplicidad de parámetros técnicos.
* `SimuladorMonteCarloEV.py`: Motor de simulación que gestiona la serie temporal (resolución de 5 minutos), propaga las condiciones ambientales, agrega la demanda de los segmentos y extrae las estadísticas de la red.


* `VehiculoSegmento.py`: Encapsula el comportamiento físico, termodinámico y estocástico a nivel de unidad individual (ajustes por temperatura, distribuciones de distancia y decisiones de carga).



## ⚙️ Metodología y Lógica de Simulación

La simulación itera a lo largo de un horizonte temporal configurable (30 días por defecto) bajo los siguientes principios físicos y probabilísticos:

1. **Resolución Temporal de Alta Precisión:** Utiliza intervalos de 5 minutos (288 pasos diarios) para capturar los picos instantáneos de demanda máxima coincidente.


2. **Modelado Termodinámico (Factor de Temperatura):** Integra la afectación de la temperatura ambiente sobre la química de las baterías tomando como referencia una temperatura óptima de operación ($21.5\text{ °C}$). Las desviaciones térmicas penalizan tanto el consumo específico en ruta ($\text{kWh/km}$) por resistencia interna y climatización, como la eficiencia de rectificación durante la recarga ($\eta_{\text{AC}}$) por activación de sistemas de gestión térmica.


3. **Restricciones Físicas de Batería:** Establece un límite de descarga neta del 90%, asumiendo que el Estado de Carga (SOC) nunca desciende del 10%.


4. **Distribuciones Estadísticas de Conducción:**
* **Uso Privado:** Aplica una distribución log-normal parametrizada para modelar la asimetría típica de recorridos urbanos diarios con viajes largos ocasionales.


* **Flotillas:** Aplica una distribución normal para representar rutas operativas estructuradas.




5. **Desplazamiento Estocástico (Shifting):** Si un vehículo finaliza el día 
con un SOC superior al 50%, existe un 60% de probabilidad de que posponga su conexión para el día siguiente.



## 📊 Escenarios de Penetración

Los escenarios preconfigurados en `escenarios.py` representan distintos niveles de adopción respecto a la línea base territorial:

* `Conservador`: Incremento del 20% respecto a la línea base (9 VE, 3 PHEV).


* `Tendencial`: Incremento del 40% (11 VE, 3 PHEV).


* `Acelerado`: Incremento del 80%, consistente con el crecimiento histórico reciente de la demarcación (14 VE, 4 PHEV).


* `Sensibilidad`: Escenario exploratorio de estrés límite (35 VE, 10 PHEV) diseñado para evaluar la saturación del transformador.


* `Example`: Muestra de control masiva con 133 vehículos distribuidos en los 10 modelos representativos del mercado mexicano.



## 🚀 Instalación y Ejecución (CLI)

Se requiere **Python 3.8 o superior**. Para instalar la herramienta y habilitar el comando en la terminal, seguir estos pasos:

1. Clonar el repositorio y acceder al directorio raíz del proyecto.
2. Instalar el paquete en modo editable (esto instalará automáticamente `numpy`, `pandas` y `matplotlib`):
```bash
pip install -e .
```



### Comandos de Uso

Una vez instalado, el simulador se ejecuta directamente desde cualquier terminal mediante el comando `prelectrics`:

 Argumentos disponibles:

* `-e`, `--escenario` **(Obligatorio):** Nombre del escenario a simular (`Conservador`, `Tendencial`, `Acelerado`, `Sensibilidad`, `Example`).
* `-t`, `--temperatura` *(Opcional):* Temperatura ambiente media en °C (Valor por defecto: `16.0`).
* `-d`, `--dias` *(Opcional):* Horizonte de días a simular (Valor por defecto: `30`).

**Ejemplos de ejecución:**

```bash
# Ejecución estándar (30 días a 16.0 °C)
prelectrics --escenario Conservador

# Simulación del escenario acelerado en condiciones invernales durante 15 días
prelectrics --escenario Acelerado --temperatura 13.5 --dias 15

# Ejecución abreviada para prueba de estrés en clima cálido durante una semana
prelectrics -e Sensibilidad -t 26.0 -d 7

# Consultar el menú de ayuda en consola
prelectrics --help

```

Al finalizar la corrida, el sistema imprime en consola el resumen técnico (Temperatura, Demanda Máxima Coincidente, Demanda Promedio, Demanda Mínima, Factor de Carga y Energía Total Demandada) y despliega el gráfico de áreas apiladas del perfil de potencia resultante.