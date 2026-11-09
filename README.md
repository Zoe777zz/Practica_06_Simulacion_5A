# Práctica 06 - Validación estadística de números pseudoaleatorios

**Asignatura:** Simulación | **Lenguajes:** Python y Java | **Sistema operativo:** Linux (Ubuntu, Debian y derivados).

Este proyecto implementa el **generador congruencial lineal (LCG)** en Python y Java. Evalúa la uniformidad de los números pseudoaleatorios con las pruebas **Chi-cuadrado** (10 intervalos y 9 grados de libertad) y **Kolmogorov-Smirnov (KS)**, con un nivel de significancia de **0,05**. Incluye dos configuraciones del generador, tablas, archivos CSV y gráficas.

También se realiza una **comparación complementaria** entre Python y Java: tiempos de ejecución y estimación de π mediante Monte Carlo, como se solicita en la tabla de resultados esperados de la guía. La estimación de π no sustituye las pruebas de uniformidad.

## 1. Requisitos en Linux

Se necesita:

- Git, para clonar y actualizar el repositorio.
- Python 3.10 o superior.
- Java JDK 17 o superior (`javac` y `java`).
- Conexión a internet para clonar el repositorio e instalar las dependencias de Python.

En Ubuntu o Debian, instalar con:

```bash
sudo apt update
sudo apt install -y git python3 python3-venv python3-pip openjdk-17-jdk
```

Para comprobar la instalación:

```bash
git --version
python3 --version
java -version
javac -version
```

## 2. Clonar el repositorio desde GitHub

Abre una terminal y ve a la carpeta donde quieras guardar el proyecto, por ejemplo, `Documentos`:

```bash
cd ~/Documentos
```

**Reemplaza `TU_USUARIO/TU_REPOSITORIO` por la dirección real del repositorio de la Práctica 06 en GitHub.**

```bash
git clone https://github.com/TU_USUARIO/TU_REPOSITORIO.git Practica_06_Uniformidad
cd Practica_06_Uniformidad
```

El segundo argumento de `git clone` hace que la carpeta local se llame `Practica_06_Uniformidad`, independientemente del nombre que tenga el repositorio en GitHub.

> Solo hay que clonar la primera vez. En las siguientes ocasiones, entra a la carpeta local y usa `git pull` para traer los cambios publicados en la rama actual:
>
> ```bash
> cd ~/Documentos/Practica_06_Uniformidad
> git pull
> ```
>
> Si el repositorio es privado, GitHub solicitará que tengas acceso y te autentiques.

## 3. Crear el entorno virtual e instalar dependencias

Desde la **carpeta principal** del proyecto clonado:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

Al activar el entorno virtual aparecerá `(.venv)` al principio de la terminal. La instalación de dependencias solo es necesaria la primera vez o cuando cambie `requirements.txt`.

Cuando abras otra terminal para trabajar, entra en el proyecto y vuelve a activar el entorno:

```bash
cd ~/Documentos/Practica_06_Uniformidad
source .venv/bin/activate
```

## 4. Ejecutar el análisis estadístico en Python

```bash
python python/practica06.py
```

Por defecto, genera **10 000 números** para la configuración buena y otros **10 000** para la mala, utilizando la **semilla 2026**. Aplica Chi-cuadrado y KS, muestra los estadísticos, valores p y decisiones, y guarda los archivos en:

- `resultados/python_buena/secuencia.csv`: estados y números normalizados.
- `resultados/python_buena/frecuencias.csv`: frecuencias observadas y esperadas.
- `resultados/python_buena/pruebas.csv`: resultados y decisiones estadísticas.
- `resultados/python_buena/frecuencias.png`: gráfica de frecuencias.
- `resultados/python_buena/acumulada.png`: distribución acumulada empírica y teórica.
- En `resultados/python_mala/` se guardan los archivos equivalentes.

Para elegir la cantidad de números, semilla o configuración:

```bash
python python/practica06.py --n 10000 --semilla 2026 --config buena
python python/practica06.py --n 10000 --semilla 2026 --config mala
python python/practica06.py --help
```

**Importante:** utiliza al menos 50 datos para que, con 10 intervalos, la frecuencia esperada sea como mínimo 5 por intervalo.

## 5. Ejecutar el análisis estadístico en Java

Desde la carpeta principal del proyecto clonado:

```bash
mkdir -p java/bin
javac -encoding UTF-8 -d java/bin java/Generador.java java/Practica06.java
java -cp java/bin Practica06 analizar buena 10000 2026 resultados/java_buena
java -cp java/bin Practica06 analizar mala 10000 2026 resultados/java_mala
```

- `java/Generador.java` implementa el LCG y sus configuraciones.
- `java/Practica06.java` utiliza el generador y aplica Chi-cuadrado y KS.
- Los archivos CSV se guardan en `resultados/java_buena/` y `resultados/java_mala/`.

Los dos archivos `.java` deben compilarse juntos. Java utiliza el mismo algoritmo LCG y los mismos parámetros que Python. **El valor p de KS en Java es una aproximación asintótica**, por lo que puede variar ligeramente respecto del cálculo con SciPy. Las gráficas PNG se generan con Python.

## 6. Comparar Python y Java

Con el entorno virtual activado:

```bash
python comparar.py
```

Este programa compila automáticamente los archivos Java y compara las dos implementaciones para **N = 1 000, 10 000, 100 000 y 1 000 000**. También estima π mediante Monte Carlo y registra el tiempo de cálculo de ambos lenguajes.

La tabla se guarda en:

```text
resultados/comparacion_python_java.csv
```

- `pi_estimado`: valor aproximado de π.
- `error_absoluto`: diferencia entre el valor estimado y π.
- `tiempo_python_ms` y `tiempo_java_ms`: tiempo medido en milisegundos (mediana de tres ejecuciones).
- `checksum`: suma de control de los estados del generador.
- `identicas`: indica que coinciden los *checksums* y las estimaciones comprobadas por el programa. Es una verificación práctica, pero un *checksum* coincidente por sí solo no demuestra la igualdad elemento a elemento.

Los tiempos no incluyen la compilación ni el arranque del intérprete o la JVM y pueden variar entre equipos.

## 7. Interpretación de las pruebas

- **H₀:** los datos siguen una distribución uniforme U(0,1).
- **H₁:** los datos no siguen una distribución uniforme U(0,1).
- **Si p ≥ 0,05:** no se rechaza H₀.
- **Si p < 0,05:** se rechaza H₀.
- **Chi-cuadrado:** compara las frecuencias observadas con las esperadas (`N / 10`).
- **Kolmogorov-Smirnov:** calcula la mayor diferencia entre la distribución acumulada empírica y la uniforme teórica.

**No rechazar H₀ no demuestra que la secuencia sea verdaderamente aleatoria ni independiente.**

## 8. Estructura del proyecto

```text
Practica_06_Uniformidad/
├── README.md
├── requirements.txt
├── comparar.py
├── .gitignore
├── python/
│   ├── generador.py
│   └── practica06.py
├── java/
│   ├── Generador.java
│   └── Practica06.java
└── resultados/
    ├── python_buena/
    ├── python_mala/
    ├── java_buena/
    ├── java_mala/
    └── comparacion_python_java.csv
```

Las carpetas de resultados se crean o actualizan al ejecutar los análisis; no es obligatorio descargarlas previamente desde GitHub.

## 9. Problemas comunes

- **`git: command not found`:** ejecuta `sudo apt install git`.
- **`Repository not found`:** comprueba que reemplazaste la URL de ejemplo por la real y que tienes acceso al repositorio.
- **`destination path ... already exists`:** no vuelvas a clonar sobre una carpeta existente; entra en ella y utiliza `git pull` si ya es tu copia del repositorio.
- **`python: command not found`:** activa el entorno virtual o utiliza `python3`.
- **`No module named scipy` / `matplotlib`:** activa `.venv` y ejecuta `python -m pip install -r requirements.txt`.
- **`javac: command not found`:** instala el JDK con `sudo apt install openjdk-17-jdk`.
- **`Could not find or load main class Practica06`:** compila ambas clases y ejecuta Java desde la carpeta principal usando `-cp java/bin`.

## 10. Declaración de uso de IA

Se utilizó ChatGPT, desarrollado por OpenAI, como apoyo para organizar el código, documentar el procedimiento y redactar este README. La revisión, ejecución, comprensión y presentación académica corresponden al estudiante.
