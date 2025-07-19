

public class TanTest {
    public static void main (String[] args) {
        int count = 0;
        long max = (long) Math.pow(10, 15)+1;
        for (long i = 0; i<max; i++) {
            if (Math.tan(i)>i) {
                count++;
            }
        }

        System.out.println(count);
    }
}