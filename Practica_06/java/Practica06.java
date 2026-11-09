import java.io.BufferedWriter;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.Arrays;
import java.util.Locale;

/** Practica 06. Pruebas estadisticas en Java 17+ sin librerias externas. */
public class Practica06 {
    static final int K = 10;
    static final double ALFA = 0.05;
    static final long M_CHECKSUM = 1000000007L;

    // Funcion Gamma logaritmica (coeficientes Lanczos).
    static double logGamma(double z) {
        double[] p = {0.99999999999980993, 676.5203681218851,
            -1259.1392167224028, 771.32342877765313, -176.6150291621406,
            12.507343278686905, -0.13857109526572012,
            9.984369578019572e-6, 1.5056327351493116e-7};
        if (z < 0.5) {
            return Math.log(Math.PI) - Math.log(Math.sin(Math.PI * z)) - logGamma(1 - z);
        }
        z -= 1;
        double x = p[0];
        for (int i = 1; i < p.length; i++) x += p[i] / (z + i);
        double t = z + 7.5;
        return 0.5 * Math.log(2 * Math.PI) + (z + 0.5) * Math.log(t) - t + Math.log(x);
    }

    // Cola de distribucion Gamma regularizada Q(a,x): p de Chi-cuadrado.
    static double gammaQ(double a, double x) {
        if (x <= 0) return 1.0;
        double factor = Math.exp(-x + a * Math.log(x) - logGamma(a));
        if (x < a + 1) {
            double suma = 1 / a;
            double termino = suma;
            for (int i = 1; i <= 500; i++) {
                termino *= x / (a + i);
                suma += termino;
                if (Math.abs(termino) < Math.abs(suma) * 1e-14) break;
            }
            return Math.max(0, Math.min(1, 1 - suma * factor));
        }
        double b = x + 1 - a, c = 1e300, d = 1 / b, h = d;
        for (int i = 1; i <= 500; i++) {
            double an = -i * (i - a);
            b += 2;
            d = an * d + b;
            if (Math.abs(d) < 1e-300) d = 1e-300;
            c = b + an / c;
            if (Math.abs(c) < 1e-300) c = 1e-300;
            d = 1 / d;
            double delta = d * c;
            h *= delta;
            if (Math.abs(delta - 1) < 1e-14) break;
        }
        return Math.max(0, Math.min(1, factor * h));
    }

    // Aproximacion asintotica clasica al valor p de KS.
    static double pKS(double d, int n) {
        if (d <= 0) return 1.0;
        double raiz = Math.sqrt(n);
        double lambda = (raiz + 0.12 + 0.11 / raiz) * d;
        double suma = 0;
        for (int j = 1; j <= 100; j++) {
            double t = 2 * (j % 2 == 1 ? 1 : -1) * Math.exp(-2 * j * j * lambda * lambda);
            suma += t;
            if (j > 1 && Math.abs(t) < 1e-15) break;
        }
        return Math.max(0, Math.min(1, suma));
    }

    static void comparar(String conf, int n, long semilla) {
        if (n <= 0 || n % 2 != 0) throw new IllegalArgumentException("N debe ser positivo y par");
        Generador generador = new Generador(conf, semilla);
        long checksum = 0;
        int adentro = 0;
        double x = 0;
        long inicio = System.nanoTime();
        for (int i = 0; i < n; i++) {
            long estado = generador.siguienteEstado();
            checksum = (checksum * 31 + estado) % M_CHECKSUM;
            double v = generador.normalizar(estado);
            if (i % 2 == 0) x = v;
            else if (x * x + v * v <= 1.0) adentro++;
        }
        double milisegundos = (System.nanoTime() - inicio) / 1e6;
        double pi = 4.0 * adentro / (n / 2.0);
        System.out.printf(Locale.US, "RESULTADO;%d;%.12f;%.12f;%.6f;%d%n",
                n, pi, Math.abs(Math.PI - pi), milisegundos, checksum);
    }

    static void analizar(String conf, int n, long semilla, Path carpeta) throws IOException {
        if (n < 50) throw new IllegalArgumentException("N debe ser >= 50");
        Files.createDirectories(carpeta);
        Generador generador = new Generador(conf, semilla);
        double[] numeros = new double[n];
        int[] frecuencias = new int[K];
        try (BufferedWriter f = Files.newBufferedWriter(carpeta.resolve("secuencia.csv"))) {
            f.write("posicion,estado,numero\n");
            for (int i = 0; i < n; i++) {
                long estado = generador.siguienteEstado();
                double numero = generador.normalizar(estado);
                numeros[i] = numero;
                frecuencias[Math.min(K - 1, (int) (numero * K))]++;
                f.write(String.format(Locale.US, "%d,%d,%.9f%n", i + 1, estado, numero));
            }
        }
        double esperado = (double) n / K;
        double chi2 = 0;
        for (int f : frecuencias) chi2 += (f - esperado) * (f - esperado) / esperado;
        double pChi2 = gammaQ((K - 1) / 2.0, chi2 / 2);
        Arrays.sort(numeros);
        double d = 0;
        for (int i = 0; i < n; i++) {
            d = Math.max(d, (i + 1.0) / n - numeros[i]);
            d = Math.max(d, numeros[i] - i / (double) n);
        }
        double pKs = pKS(d, n);
        try (BufferedWriter f = Files.newBufferedWriter(carpeta.resolve("frecuencias.csv"))) {
            f.write("intervalo,observada,esperada\n");
            for (int i = 0; i < K; i++) {
                f.write(String.format(Locale.US, "\"[%.1f, %.1f)\",%d,%.1f%n",
                    i / 10.0, (i + 1) / 10.0, frecuencias[i], esperado));
            }
        }
        String descChi = pChi2 >= ALFA ? "No se rechaza H0" : "Se rechaza H0";
        String descKs = pKs >= ALFA ? "No se rechaza H0" : "Se rechaza H0";
        try (BufferedWriter f = Files.newBufferedWriter(carpeta.resolve("pruebas.csv"))) {
            f.write("prueba,estadistico,p,decision\n");
            f.write(String.format(Locale.US, "Chi-cuadrado,%.9f,%.12g,%s%n", chi2, pChi2, descChi));
            f.write(String.format(Locale.US, "Kolmogorov-Smirnov,%.9f,%.12g,%s%n", d, pKs, descKs));
        }
        System.out.println("LCG " + conf + " | N=" + n + " | semilla=" + semilla);
        System.out.printf(Locale.US, "Chi2=%.6f; p=%.8g; %s%n", chi2, pChi2, descChi);
        System.out.printf(Locale.US, "KS D=%.6f; p aprox=%.8g; %s%n", d, pKs, descKs);
        System.out.println("Resultados en: " + carpeta);
    }

    public static void main(String[] args) throws Exception {
        if (args.length < 1) {
            System.out.println("Uso: java Practica06 analizar buena 10000 2026 resultados/java_buena");
            System.out.println("   o: java Practica06 comparar buena 10000 2026");
            return;
        }
        String modo = args[0];
        String conf = args.length >= 2 ? args[1] : "buena";
        int n = args.length >= 3 ? Integer.parseInt(args[2]) : 10000;
        long semilla = args.length >= 4 ? Long.parseLong(args[3]) : 2026;
        if (modo.equals("comparar")) comparar(conf, n, semilla);
        else if (modo.equals("analizar")) {
            Path carpeta = Path.of(args.length >= 5 ? args[4] : "resultados/java_" + conf);
            analizar(conf, n, semilla, carpeta);
        } else throw new IllegalArgumentException("Modo: analizar o comparar");
    }
}
