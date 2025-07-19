import java.util.HashMap;
import java.math.BigInteger;

public class FibTest
{
    
    public static void main(String[] args)
    {
        HashMap<Integer, BigInteger> fibs= new HashMap<Integer, BigInteger>();
    
        fibs.put(1,BigInteger.ZERO);
        fibs.put(2, BigInteger.ONE);
        
        
        for (int i = 1; i <= 1000000; i++) {

            if (i%10000 == 0) {
                System.out.println(i + ". "+  fib(i,fibs) + " -- " + i);
            }
        }
    }
    
    public static BigInteger fib(int n, HashMap<Integer, BigInteger> fibs) {
        if (n<1) {
            return BigInteger.valueOf(-1);
        }
        else if (n<=fibs.size()) {
            System.out.println("Already calculated.");
            return fibs.get(n);
        }
        
        else {
            for (int i = fibs.size()+1; i<=n; i++) {
                fibs.put(i,fibs.get(i-1).add(fibs.get(i-2)));
            }
            
            return fibs.get(n);
        }
    }
    
}
