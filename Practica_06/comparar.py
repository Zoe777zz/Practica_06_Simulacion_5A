"""Compara las implementaciones Python y Java con identica secuencia LCG."""

import csv
import math
from pathlib import Path
import statistics
import subprocess
import sys
from time import perf_counter

sys.path.insert(0, str(Path(__file__).parent / "python"))
from generador import generar

RAIZ = Path(__file__).resolve().parent
SEMILLA = 2026
CANTIDADES = [1000, 10000, 100000, 1000000]
REPETICIONES = 3


def python_comparacion(n, conf):
    inicio = perf_counter()
    checksum = 0
    dentro = 0
    x = None
    for estado, valor in generar(n, SEMILLA, conf):
        checksum = (checksum * 31 + estado) % 1000000007
        if x is None:
            x = valor
        else:
            if x * x + valor * valor <= 1:
                dentro += 1
            x = None
    tiempo = (perf_counter() - inicio) * 1000
    estimacion = 4 * dentro / (n / 2)
    return estimacion, abs(math.pi - estimacion), tiempo, checksum


def java_comparacion(n, conf):
    comando = ["java", "-cp", str(RAIZ / "java" / "bin"),
               "Practica06", "comparar", conf, str(n), str(SEMILLA)]
    salida = subprocess.check_output(comando, text=True).strip()
    datos = salida.split(";")
    if len(datos) != 6 or datos[0] != "RESULTADO" or int(datos[1]) != n:
        raise RuntimeError("Salida Java inesperada: " + salida)
    return float(datos[2]), float(datos[3]), float(datos[4]), int(datos[5])


def main():
    (RAIZ / "java" / "bin").mkdir(parents=True, exist_ok=True)
    subprocess.run(["javac", "-encoding", "UTF-8", "-d", str(RAIZ / "java" / "bin"),
                    str(RAIZ / "java" / "Generador.java"),
                    str(RAIZ / "java" / "Practica06.java")], check=True)
    destino = RAIZ / "resultados"
    destino.mkdir(exist_ok=True)
    filas = []
    for conf in ("buena", "mala"):
        for n in CANTIDADES:
            python_runs = [python_comparacion(n, conf) for _ in range(REPETICIONES)]
            java_runs = [java_comparacion(n, conf) for _ in range(REPETICIONES)]
            p, j = python_runs[0], java_runs[0]
            if p[3] != j[3] or not math.isclose(p[0], j[0], abs_tol=1e-10):
                raise AssertionError(f"Secuencias distintas: {conf}, n={n}")
            fila = (conf, n, f"{p[0]:.8f}", f"{p[1]:.8f}",
                    f"{statistics.median(x[2] for x in python_runs):.3f}",
                    f"{statistics.median(x[2] for x in java_runs):.3f}",
                    p[3], "SI")
            filas.append(fila)
            print("Config={:<5} N={:<7} pi={:<11} error={:<11} Python={}ms Java={}ms OK".format(*fila[:6]))
    with open(destino / "comparacion_python_java.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["configuracion", "N", "pi_estimado", "error_absoluto",
                         "tiempo_python_ms", "tiempo_java_ms", "checksum", "identicas"])
        writer.writerows(filas)
    print("\nComparacion guardada en resultados/comparacion_python_java.csv")


if __name__ == "__main__":
    main()
