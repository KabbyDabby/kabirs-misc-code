from math import floor
ret = 0
for i in range(101):
    ret+=floor(i**(3/2))

for i in range(1001):
    ret+=floor(i**(2/3))

print(ret)