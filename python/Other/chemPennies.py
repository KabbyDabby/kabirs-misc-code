from math import ceil, floor

for i in range(100001): # reactant pennies to start with
    r = i
    p = 100000-r

    for _ in range(1000):
        p += ceil(r//2)
        r = floor(r/2)

        r+=ceil(p/4)
        p = p-ceil(p/4)
    
    
    print(p/r)
