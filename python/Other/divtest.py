from time import perf_counter as time



num = 10**8

start1 = time()
x=0
for i in range(1,num):
    x+= int((i*i)/i)

print(time()-start1)



start2 = time()
x=0

for i in range(1,num):
    x+= (i*i)//i
#results, // is about 20-25% faster than int(/)
print(time()-start2)