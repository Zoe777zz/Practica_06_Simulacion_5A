
# Practica 06 - Validacion estadistica de numeros pseudoaleatorios

**Asignatura:** Simulacion | **Lenguajes:** Python y Java | **Sistema:** Linux (Ubuntu, Debian y derivados).

Se implementa el **generador congruencial lineal (LCG)** en Python y Java. Se comprueba la uniformidad con **Chi-cuadrado** (10 intervalos, 9 grados de libertad) y **Kolmogorov-Smirnov**, usando un nivel de significancia de 0.05. Se comparan dos configuraciones y se generan graficas, tablas y CSV.

El PDF de la practica, en la seccion 6, agrega una tabla con **pi estimado, error y tiempos de Python/Java**, aunque ese indicador no pertenece a las pruebas de uniformidad. Por eso se incluye como **comparacion complementaria** por el metodo de Monte Carlo, sin reemplazar las pruebas principales.

## 1. Requisitos en Linux

- Python 3.10 o superior.
- Java JDK 17 o superior (incluye los comandos `javac` y `java`).
- Conexion a internet **solo** para instalar las librerias de Python la primera vez.

```bash
sudo apt update
sudo apt install -y python3 python3-venv python3-pip openjdk-17-jdk unzip
```

Si el equipo ya tiene Python 3 y JDK instalados, omite ese paso.

## 2. Descomprimir y entrar al proyecto

Guarda el ZIP en la carpeta `Descargas` y ejecuta:

```bash
cd ~/Descargas
unzip Practica_06_Uniformidad.zip
cd Practica_06_Uniformidad
```

> Si abres una terminal dentro de la carpeta descomprimida, puedes omitir los `cd` anteriores.

## 3. Crear el entorno virtual e instalar dependencias

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

Al activarlo aparecera `(.venv)` al comienzo de la terminal. Solo necesitas instalar las dependencias una vez.

## 4. Ejecutar el analisis estadistico en Python

```bash
python python/practica06.py
```

**Hace lo siguiente:** genera 10 000 numeros para la configuracion buena y 10 000 para la mala (semilla 2026), ejecuta Chi-cuadrado y KS, imprime el valor p y la decision, y guarda los resultados en:

- `resultados/python_buena/secuencia.csv`: cada estado y su numero normalizado.
- `resultados/python_buena/frecuencias.csv`: frecuencias observadas y esperadas.
- `resultados/python_buena/pruebas.csv`: estadisticos, valores p y decisiones.
- `resultados/python_buena/frecuencias.png`: grafica de barras.
- `resultados/python_buena/acumulada.png`: curva empirica y teorica.
- Archivos equivalentes en `resultados/python_mala/`.

Para cambiar la cantidad, semilla o configuracion:

```bash
python python/practica06.py --n 10000 --semilla 2026 --config buena
python python/practica06.py --n 10000 --semilla 2026 --config mala
python python/practica06.py --help
```

**Importante:** usa al menos 50 datos: en 10 intervalos, la frecuencia esperada debe ser al menos 5.

## 5. Ejecutar la implementacion Java

Desde la carpeta principal del proyecto:

```bash
mkdir -p java/bin
javac -encoding UTF-8 -d java/bin java/Generador.java java/Practica06.java
java -cp java/bin Practica06 analizar buena 10000 2026 resultados/java_buena
java -cp java/bin Practica06 analizar mala 10000 2026 resultados/java_mala
```

Los archivos CSV estaran en `resultados/java_buena/` y `resultados/java_mala/`. `Generador.java` contiene la formula LCG y las dos configuraciones. `Practica06.java` utiliza ese generador y aplica Chi-cuadrado y KS. Ambas clases se compilan juntas. La implementacion Java usa la misma formula y parametros LCG. Calcula Chi-cuadrado y KS con el mismo estadistico que Python. **El valor p de KS en Java es una aproximacion asintotica**, por lo que puede variar ligeramente frente al calculo de SciPy en Python.

## 6. Generar la tabla comparativa Python vs. Java

```bash
python comparar.py
```

El programa compila `Generador.java` y `Practica06.java` automaticamente, ejecuta los dos generadores para `N = 1000, 10000, 100000 y 1000000`, verifica la identidad mediante una suma de control (`checksum`) de **toda** la secuencia, calcula una estimacion de pi con puntos Monte Carlo y guarda:

`resultados/comparacion_python_java.csv`

La columna `identicas=SI` significa que las dos implementaciones produjeron exactamente la misma secuencia de estados para esa corrida. **Los tiempos estan medidos en milisegundos** y se presenta la mediana de 3 ejecuciones. Miden solo el calculo dentro de cada programa, no la compilacion ni la carga del interprete o la JVM; pueden variar segun la computadora y el estado del sistema.

## 7. Como se interpreta

- **H0:** los valores son compatibles con una distribucion uniforme U(0,1).
- **H1:** los valores no siguen una distribucion uniforme U(0,1).
- **Si p >= 0.05:** no se rechaza H0.
- **Si p < 0.05:** se rechaza H0.
- **Chi-cuadrado:** compara la cantidad de numeros de cada intervalo con la frecuencia esperada `N / 10`.
- **KS:** mide la mayor diferencia entre distribucion acumulada empirica y teorica.
- No rechazar H0 **no demuestra** aleatoriedad verdadera ni independencia de la secuencia.

## 8. Archivos importantes

```text
Practica_06_Uniformidad/
├── README.md
├── requirements.txt
├── comparar.py
├── python/
│   ├── generador.py
│   └── practica06.py
├── java/
│   ├── Generador.java       # Genera los numeros con LCG
│   └── Practica06.java      # Realiza las pruebas estadisticas
└── resultados/
    ├── python_buena/
    ├── python_mala/
    ├── java_buena/
    ├── java_mala/
    └── comparacion_python_java.csv
```

### Problemas comunes

- **`python: command not found`**: usa `python3` o activa el entorno virtual con `source .venv/bin/activate`.
- **`No module named scipy/matplotlib`**: verifica el entorno virtual y ejecuta `python -m pip install -r requirements.txt`.
- **`javac: command not found`**: instala el JDK con `sudo apt install openjdk-17-jdk`.
- **`Could not find or load main class Practica06`**: compila el archivo y ejecuta Java desde la carpeta principal, usando `-cp java/bin`.

## 9. Declaratoria de IA

Se utilizo ChatGPT (OpenAI) como apoyo para estructurar el codigo, el documento y este README. La ejecucion, comprension, revision y presentacion academica corresponden al estudiante.
