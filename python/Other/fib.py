from time import perf_counter as time
from math import log10 as log

def fib(n,start):
    table = {0:0,1:1}
    for i in range(2,n+1):
        if i%10000 == 0:
            print(i//10000)
        table[i] = table[i-1]+table[i-2]
    print(time()-start)
    return table[n-1]
start = time()
# print(log(fib(750000)))
fib(750000,start)
# print(time()-start)