primes = [2]
for i in range(3,2000,2):
    if 0 not in [i % j for j in primes]:
        primes.append(i)

def primeFactors(n):
    factors = []
    num = n
    for i in primes:
        if num % i == 0: factors.append(i)
        while num % i == 0: num = num / i
        if num == 1: break
    return factors

def tao(n):
    num = n
    primePowers = []
    pF = primeFactors(n)
    for i in range(0,len(pF)):
        primePowers.append(0)
        while num % pF[i] == 0:
            num = num / pF[i]
            primePowers[i] += 1
    value = 1
    for i in range(0,len(primePowers)):
        value *= 1 + primePowers[i]
    return value

tau = []
for i in range(1,2000):
    tau.append(tao(i))

def sols(k,a,b,l):
    numOfSolutions = 0
    for i in range(a,b):
        if l[i-1] == l[i+k-1]: numOfSolutions += 1
    return numOfSolutions

def solList(k,a,b,l):
    li = []
    for i in range(a,b):
        if l[i-1] == l[i+k-1]: li.append(i)
    return list
    
def maxSolFound(k,a,b,l):
    return max(solList(k,a,b,l))

for i in range(1,100):
    print(solList(i,1,1000,tau))
    # print(f"{i}: {solList(i,1,1000,tau)}")