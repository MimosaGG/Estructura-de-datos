import java.util.Random;

public class Lista {
    private String[] meses;
    private String[] departamentos;
    private int[][] matriz;
    private Random random;

    public Lista() {
        this.meses = new String[]{
            "Enero", "Febrero", "marzo", "abril", "mayo", "junio", 
            "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre"
        };
        
        this.departamentos = new String[]{"Deportes", "Ropa", "jugueteria"};
        
        this.matriz = new int[12][3];
        this.random = new Random();
        
        
        for (int i = 0; i < 12; i++) {
            for (int j = 0; j < 3; j++) {
                this.matriz[i][j] = this.random.nextInt(1500 - 27 + 1) + 27;
            }
        }
    }

    public void mostrarTabla() {
      
        System.out.printf("%-12s | ", "Mes");
        for (int i = 0; i < departamentos.length; i++) {
            System.out.printf("%-12s", departamentos[i]);
            if (i < departamentos.length - 1) {
                System.out.print(" | ");
            }
        }
        System.out.println();
        System.out.println("-".repeat(55));

        
        for (int i = 0; i < meses.length; i++) {
            System.out.printf("%-12s | ", meses[i]);
            for (int j = 0; j < matriz[i].length; j++) {
                System.out.printf("%-12d", matriz[i][j]);
                if (j < matriz[i].length - 1) {
                    System.out.print(" | ");
                }
            }
            System.out.println();
        }
        System.out.println("-".repeat(55));
    }

    public void insertarVenta(int mesIdentificador, int depIdentificador, int valor) {
        if (mesIdentificador >= 0 && mesIdentificador < 12 && depIdentificador >= 0 && depIdentificador < 3) {
            this.matriz[mesIdentificador][depIdentificador] = valor;
            System.out.println("Venta actualizada: " + this.meses[mesIdentificador] + " - " + this.departamentos[depIdentificador] + " = " + valor);
        } else {
            System.out.println("Índice de mes o departamento fuera de rango.");
        }
    }

    public void buscarVenta(int valor) {
        boolean encontrado = false;
        for (int i = 0; i < 12; i++) {
            for (int j = 0; j < 3; j++) {
                if (this.matriz[i][j] == valor) {
                    System.out.println("El valor " + valor + " está en el mes de " + this.meses[i] + ", departamento " + this.departamentos[j] + ".");
                    encontrado = true;
                }
            }
        }
        if (!encontrado) {
            System.out.println("El valor " + valor + " no se encuentra registrado en la matriz.");
        }
    }

    public void eliminarVenta(int mesIdx, int depIdx) {
        if (mesIdx >= 0 && mesIdx < 12 && depIdx >= 0 && depIdx < 3) {
            int anterior = this.matriz[mesIdx][depIdx];
            this.matriz[mesIdx][depIdx] = 0;
            System.out.println("Eliminado la venta de " + this.meses[mesIdx] + " en " + this.departamentos[depIdx] + " (valor anterior: " + anterior + ").");
        } else {
            System.out.println("No se encuentra en el rango papu");
        }
    }

    public static void main(String[] args) {
        Lista sistema = new Lista();
        sistema.mostrarTabla();

        System.out.println("\nBúsqueda");
        sistema.buscarVenta(504); 

        System.out.println("\ninsertar");
        sistema.insertarVenta(0, 1, 480);

        System.out.println("\nEliminacion");
        sistema.eliminarVenta(0, 1);
    }
}
