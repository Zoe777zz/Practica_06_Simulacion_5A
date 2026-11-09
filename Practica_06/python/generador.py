"""Generador congruencial lineal (LCG). Sin dependencias externas."""

CONFIGURACIONES = {
    # LCG de 32 bits. Se usa como ejemplo de mejor dispersion.
    "buena": (1664525, 1013904223, 2**32),
    # Modulo pequeno para mostrar el efecto de un periodo muy corto.
    "mala": (5, 1, 16),
}


def generar(n=10000, semilla=2026, configuracion="buena"):
    """Devuelve (estado entero, numero [0,1)) en cada iteracion."""
    if configuracion not in CONFIGURACIONES:
        raise ValueError("Configuracion valida: buena o mala")
    if n <= 0:
        raise ValueError("n debe ser mayor que cero")
    a, c, m = CONFIGURACIONES[configuracion]
    estado = semilla % m
    for _ in range(n):
        estado = (a * estado + c) % m
        yield estado, estado / m
