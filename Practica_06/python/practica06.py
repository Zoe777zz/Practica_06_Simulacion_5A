"""Practica 06: uniformidad del LCG con Chi-cuadrado y KS."""

import argparse
import csv
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from scipy import stats

from generador import generar, CONFIGURACIONES

ALFA = 0.05
K = 10


def escribir_csv(ruta, encabezado, filas):
    with open(ruta, "w", newline="", encoding="utf-8") as archivo:
        escritor = csv.writer(archivo)
        escritor.writerow(encabezado)
        escritor.writerows(filas)


def analizar(configuracion, n, semilla, carpeta):
    carpeta.mkdir(parents=True, exist_ok=True)
    datos = list(generar(n, semilla, configuracion))
    valores = [numero for _, numero in datos]

    observadas = [0] * K
    for numero in valores:
        observadas[min(int(numero * K), K - 1)] += 1
    esperada = n / K
    chi2 = sum((f - esperada) ** 2 / esperada for f in observadas)
    p_chi2 = float(stats.chi2.sf(chi2, K - 1))

    # KS de una muestra frente a U(0,1), sin parametros estimados.
    d_ks, p_ks = stats.kstest(valores, "uniform", method="auto")
    decision_chi = "No se rechaza H0" if p_chi2 >= ALFA else "Se rechaza H0"
    decision_ks = "No se rechaza H0" if p_ks >= ALFA else "Se rechaza H0"

    escribir_csv(carpeta / "secuencia.csv", ["posicion", "estado", "numero"],
                ((i, estado, f"{numero:.9f}") for i, (estado, numero) in enumerate(datos, 1)))
    escribir_csv(carpeta / "frecuencias.csv", ["intervalo", "observada", "esperada"],
                ((f"[{i/K:.1f}, {(i+1)/K:.1f})", observadas[i], f"{esperada:.1f}")
                 for i in range(K)))
    escribir_csv(carpeta / "pruebas.csv", ["prueba", "estadistico", "p", "decision"], [
        ("Chi-cuadrado", f"{chi2:.9f}", f"{p_chi2:.12g}", decision_chi),
        ("Kolmogorov-Smirnov", f"{d_ks:.9f}", f"{p_ks:.12g}", decision_ks),
    ])

    # Figura 1: comparacion de las 10 frecuencias.
    fig, ax = plt.subplots(figsize=(9, 4.6))
    x = list(range(K))
    ax.bar(x, observadas, color="#397EB5", label="Observada")
    ax.axhline(esperada, color="#B24B5A", linewidth=2, linestyle="--", label="Esperada")
    ax.set_xticks(x, [f"{i/10:.1f}-{(i+1)/10:.1f}" for i in x], rotation=40, ha="right")
    ax.set_xlabel("Intervalo")
    ax.set_ylabel("Frecuencia")
    ax.set_title(f"Frecuencias de 10 intervalos - LCG {configuracion} (n={n:,})")
    ax.legend()
    ax.grid(axis="y", alpha=0.2)
    fig.tight_layout()
    fig.savefig(carpeta / "frecuencias.png", dpi=170)
    plt.close(fig)

    # Figura 2: funcion acumulada empirica y uniforme teorica.
    ordenados = sorted(valores)
    ecdf = [i / n for i in range(1, n + 1)]
    fig, ax = plt.subplots(figsize=(9, 4.6))
    ax.step(ordenados, ecdf, where="post", color="#397EB5", label="Acumulada empirica")
    ax.plot([0, 1], [0, 1], "--", color="#B24B5A", linewidth=2, label="Uniforme teorica")
    ax.set(xlim=(0, 1), ylim=(0, 1), xlabel="Valor x", ylabel="Probabilidad acumulada",
           title=f"Kolmogorov-Smirnov - LCG {configuracion} (D={d_ks:.5f})")
    ax.legend()
    ax.grid(alpha=0.2)
    fig.tight_layout()
    fig.savefig(carpeta / "acumulada.png", dpi=170)
    plt.close(fig)

    print(f"\nLCG {configuracion.upper()} | n={n} | semilla={semilla}")
    print(f"Parametros (a,c,m): {CONFIGURACIONES[configuracion]}")
    print("Primeros 10 numeros:", ", ".join(f"{v:.6f}" for v in valores[:10]))
    print(f"Chi2={chi2:.6f}; gl={K-1}; p={p_chi2:.8g}; {decision_chi}")
    print(f"KS D={d_ks:.6f}; p={p_ks:.8g}; {decision_ks}")
    print("Archivos en:", carpeta)
    return {
        "configuracion": configuracion, "n": n, "semilla": semilla,
        "observadas": observadas, "esperada": esperada,
        "chi2": chi2, "p_chi2": p_chi2, "d_ks": float(d_ks), "p_ks": float(p_ks),
        "decision_chi": decision_chi, "decision_ks": decision_ks,
        "primeros": valores[:10],
    }


def main():
    parser = argparse.ArgumentParser(description="Practica 06 - LCG, Chi2 y KS")
    parser.add_argument("--n", type=int, default=10000, help="Cantidad de numeros (10000)")
    parser.add_argument("--semilla", type=int, default=2026)
    parser.add_argument("--config", choices=["buena", "mala", "ambas"], default="ambas")
    parser.add_argument("--salida", default="resultados")
    args = parser.parse_args()
    if args.n < 50:
        parser.error("Use n >= 50 para mantener >= 5 datos esperados por intervalo.")
    for config in (["buena", "mala"] if args.config == "ambas" else [args.config]):
        analizar(config, args.n, args.semilla, Path(args.salida) / f"python_{config}")


if __name__ == "__main__":
    main()
