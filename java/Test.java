import java.util.HashMap;
public class Test
{
    public static void main(String[] args) 
    {
        // System.out.println("Hello World!");
        System.out.println(fib(10));
        double myDouble = (double) 1/4.0;
        System.out.println(myDouble);
        
    }

    public static int fib(int n) 
    {
        HashMap<Integer,Integer> pastFibs = new HashMap<Integer,Integer>();
        pastFibs.put(0,0);
        pastFibs.put(1,1);
        for (int i = 2; i<n; i++)
        {
            pastFibs.put(i, pastFibs.get(i-1)+pastFibs.get(i-2));
            // System.out.print(pastFibs.get(i));
            // System.out.println(" "+i);
        }    
        return pastFibs.get(n-1);
    }
}