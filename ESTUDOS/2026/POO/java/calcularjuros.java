import java.util.Scanner;
//ele deve calcular juros compostos vai ser assim a = p(1 + i)^n
public class calcularjuros {

    public static void main(String[] args) {
        try (Scanner scanner = new Scanner(System.in)) {
            System.out.print("Digite o valor principal do investimento (P): ");
            double principal = Double.parseDouble(scanner.next().replace(',', '.'));

            System.out.print("Digite a taxa de juros (r) (ex.: 5 ou 0,05): ");
            double taxaJuros = Double.parseDouble(scanner.next().replace(',', '.'));
            if (taxaJuros > 1) {
                taxaJuros /= 100.0;
            }

            System.out.print("Digite o número de períodos (n): ");
            int periodos = scanner.nextInt();

            double montante = principal;
            for (int ano = 1; ano <= periodos; ano++) {
                montante *= (1 + taxaJuros);
                System.out.printf("%d ano: %.2f%n", ano, montante);
            }
            
        }
    }

}
