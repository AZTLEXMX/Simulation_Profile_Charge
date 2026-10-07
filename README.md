# Simulador Estocástico de Perfiles de Carga de Vehículos Eléctricos (VE y PHEV)

Este repositorio contiene un modelo de simulación de Montecarlo desarrollado en Python para estimar los perfiles de carga agregados de Vehículos Eléctricos (VE) y Vehículos Híbridos Enchufables (PHEV).

El modelo computacional se basa en los lineamientos técnicos de estimación de carga de la Agencia Internacional de Energía (IEA) y emplea programación orientada a objetos (POO) para facilitar la escalabilidad y mantenimiento del código.

## 📂 Estructura del Repositorio

El código está modularizado en cuatro archivos principales:

* `main.py`: Script orquestador. Define el escenario a evaluar, inicializa el entorno de simulación y genera la salida gráfica y estadística.


* `escenarios.py`: Módulo gestor que contiene las configuraciones exactas de penetración vehicular. Se encarga de instanciar y distribuir los vehículos en el motor de simulación según el escenario seleccionado.


* `SimuladorMonteCarloEV.py`: Contiene la clase principal que gestiona el tiempo (resolución de 5 minutos), agrega la demanda de los múltiples segmentos de vehículos, extrae estadísticas de la red y genera la visualización.


* `VehiculoSegmento.py`: Define el comportamiento físico y estocástico a nivel de vehículo individual. Incluye los parámetros de batería, métricas de consumo y los algoritmos probabilísticos para distancias y ventanas de carga.



## ⚙️ Metodología y Lógica de Simulación

La simulación se ejecuta iterativamente a lo largo de un mes (30 días) para capturar la variabilidad de la demanda eléctrica bajo los siguientes principios físicos y probabilísticos:

1. **Resolución Temporal de Alta Precisión:** Se utiliza un paso de tiempo de 5 minutos para capturar adecuadamente los picos instantáneos de demanda de alta potencia.


2. **Restricciones Físicas de la Batería:** Se establece un límite de descarga del 90%, asumiendo que el Estado de Carga (SOC) nunca desciende por debajo del 10% de su capacidad nominal.


3. **Distribuciones Estadísticas de Recorrido:**
* **Uso Privado:** Se emplea una distribución log-normal (convertida a partir de una media y desviación estándar parametrizables) para modelar la conducción diaria, reflejando una alta frecuencia de viajes cortos y una baja frecuencia de viajes excepcionalmente largos.


* **Flotillas:** Se emplea una distribución normal, reflejando patrones de movilidad más regulares y estructurados.




5. **Shifting Estocástico:** Se incorpora una regla de decisión basada en el nivel de batería. Si un vehículo finaliza su recorrido con un SOC superior al 50%, existe un 60% de probabilidad de que el usuario decida no conectarlo a la red, postergando la recarga para los días posteriores.



## 📊 Escenarios de Penetración

Los escenarios preconfigurados representan incrementos respecto a una línea base territorial calculada a partir de los registros históricos (2024). Se encuentran disponibles las siguientes configuraciones:

* `Conservador`: Incremento del 20% respecto a la base estimada (9 VE, 3 PHEV).


* `Tendencial`: Incremento del 40% (11 VE, 3 PHEV).


* `Acelerado`: Incremento del 80%, consistente con la tasa de crecimiento reciente de adopción (14 VE, 4 PHEV).


* `Sensibilidad`: Escenario exploratorio con volumen arbitrario superior (ej. 30 VE, 10 PHEV) diseñado para someter el modelo de transformador a un estrés límite.


* `Example`: Muestra de control masiva basada en un ecosistema de prueba con más de 100 vehículos distribuidos en el Top 10 de modelos del mercado.



## 🚀 Uso y Ejecución

Se requiere tener instalado **Python 3.x** junto con las librerías `numpy`, `pandas` y `matplotlib`.

1. Clonar el repositorio y acceder al directorio de trabajo.
2. Abrir el archivo `main.py` y asignar el escenario deseado en la variable `ESCENARIO_ACTUAL`.


3. Ejecutar el script:
```bash
python main.py

```


4. El sistema imprimirá en consola un reporte técnico con la Demanda Máxima Coincidente, Demanda Promedio, Factor de Carga y Energía Total Demandada, seguido por el despliegue del gráfico apilado del perfil de carga.
