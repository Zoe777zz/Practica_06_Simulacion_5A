/** Genera numeros pseudoaleatorios con el metodo congruencial lineal (LCG). */
public class Generador {
    private final long a;
    private final long c;
    private final long m;
    private long estado;

    public Generador(String configuracion, long semilla) {
        if (configuracion.equals("buena")) {
            a = 1664525L;
            c = 1013904223L;
            m = 4294967296L;
        } else if (configuracion.equals("mala")) {
            a = 5L;
            c = 1L;
            m = 16L;
        } else {
            throw new IllegalArgumentException("Configuracion: buena o mala");
        }
        estado = Math.floorMod(semilla, m);
    }

    // Calcula el siguiente entero: X(n+1) = (a * X(n) + c) mod m.
    public long siguienteEstado() {
        estado = (a * estado + c) % m;
        return estado;
    }

    // Transforma el estado entero en un numero entre 0 (incluido) y 1 (excluido).
    public double normalizar(long valor) {
        return (double) valor / m;
    }
}
