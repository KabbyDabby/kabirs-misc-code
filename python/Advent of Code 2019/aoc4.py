from math import comb
from collections import Counter

low = 273025
high = 767253
#part 1
count = 0
# for i in range(273025, 767253):
#     if i%1000==0:
#         print(i)
#     if len(set(str(i)))<6:
#         if (list(str(i))) == sorted((list(str(i)))):
#             count+=1


#part 2


for i in range(273025, 767253):
    if i%1000==0:
        print(i)
    
    if 2 in dict(Counter(str(i))).values():
        if (list(str(i))) == sorted((list(str(i)))):
            count+=1


print(count)