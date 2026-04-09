import java.util.Scanner;

public class exercicio3 {
    public static void main(String[] args) {
        try (Scanner scanner = new Scanner(System.in)) {
            System.out.print("Digite a nota: ");
            int nota = scanner.nextInt();

            if (nota >= 60) {
                System.out.println("Aprovado");
            } else {
                System.out.println("Reprovado");
            }
        }
    }
}