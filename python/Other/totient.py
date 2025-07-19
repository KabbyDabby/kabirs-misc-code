def gcd(a, b):
 
    if (a == 0):
        return b
    return gcd(b % a, a)
 

def euler_totient(n):
    count = 0
    for i in range(1, n):
        if gcd(i, n) == 1:
            count += 1
    return count


for b in range(5, 1000):
    num = b**3 + 4*b**2 + 3*b + 4
    num1 = b + 4
    num2 = 3*b + 4

    if (euler_totient(num)==num1*num2):
        print(b)