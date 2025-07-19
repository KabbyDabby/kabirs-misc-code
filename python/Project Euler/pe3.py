from math import floor
def smallest_prime_factor(n):
    for i in range(2,floor(n**(1/2))):
        if n%i==0:
            return i
    else:
        return n
    
def prime_factorization(n):
    factorization = []
    last = n
    while True:
        factorization.append(smallest_prime_factor(last))
        if factorization[-1] == last:
            return factorization
        else:
            last//=factorization[-1]


print(prime_factorization(600851475143))
