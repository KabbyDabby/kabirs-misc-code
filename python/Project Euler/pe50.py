from math import floor, sqrt
def prime_check(n):
    for i in range(2,floor(sqrt(n))+1):
        if n % i == 0:
            return False
    
    return True


prime_set = []
total = 0
for i in range(2, 1000000):
    if prime_check(i):
        total +=1
        prime_set.append(i)

print('done 1')


problem_dict = {}
for i in range(len(prime_set)):
    for j in range(i):
        if True: #change
            ...




