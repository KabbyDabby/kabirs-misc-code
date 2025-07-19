from math import tan, log10, floor
count = 0
for i in range (10**9, 10**15+1):
    print(floor(log10(i)))
    if tan(i)>i:
        count+=1

print(count)