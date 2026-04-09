import java.util.Scanner;

public class exercicio4 {
   public static void main(String[] args) {
      try (Scanner scanner = new Scanner(System.in)) {
         System.out.print("Digite um número: ");
         int numero = scanner.nextInt();

         System.out.print("Digite o outro número: ");
         int numero2 = scanner.nextInt();

         double media = (numero + numero2) / 2.0;
         System.out.println("A média dos números é: " + media);
      }
   }
}