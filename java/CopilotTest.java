import java.util.HashSet;
import java.util.Set;

public class CopilotTest {
    public static void main(String[] args) {
        int count = 0;
        for (int p = 2; p < 100; p++) {
            if (isPrime(p)) {
                for (int q = 2; q < 100; q++) {
                    if (isPrime(q)) {
                        int result = p * p + q * q * q;
                        if (usesEveryDigitOnce(result)) {
                            count++;
                            System.out.println("p: " + p + ", q: " + q + ", p^2 + q^3: " + result);
                        }
                    }
                }
            }
        }
        System.out.println("Total number of pairs: " + count);
    }

    private static boolean isPrime(int num) {
        if (num <= 1) return false;
        for (int i = 2; i <= Math.sqrt(num); i++) {
            if (num % i == 0) return false;
        }
        return true;
    }

    private static boolean usesEveryDigitOnce(int num) {
        String numStr = String.valueOf(num);
        if (numStr.length() != 10) return false;
        Set<Character> digits = new HashSet<>();
        for (char c : numStr.toCharArray()) {
            if (c == '0' || !digits.add(c)) return false;
        }
        return digits.size() == 10;
    }
}