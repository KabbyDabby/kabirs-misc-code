
def nprime(n):
    primes = [2]
    last = 2
    for _ in range(n-1):
        k=1
        while True:
            for num in primes:
                if (last+k)%num == 0:
                    break
            else:
                primes.append(last+k)
                break
            k+=1
    
    return primes[-1]

print(nprime(1000))