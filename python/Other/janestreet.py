# def subtract(list):
#     temp = []
#     for i in range(1,len(list)):
#         temp.append(abs(list[i]-list[i-1]))
#     return temp

# for a in range(1,16):
#     for b in range(1,16):
#         for c in range(1,16):
#             for d in range(1,16):
#                 l = [a,b,c,3,d]
#                 if len(set(l))<5:
#                     continue
#                 l2 = subtract(l)
#                 l.extend(l2)
#                 if len(set(l))<9:
#                     continue
#                 # print(l)
#                 l3 = subtract(l2)
#                 l.extend(l3)
#                 if len(set(l))<12:
#                     continue

#                 l4 = subtract(l3)
#                 # print(l, l4)
#                 l.extend(l4)
                
#                 if len(set(l))<14:
#                     continue
#                 print(l)
#                 l5 = subtract(l4)
#                 l.extend(l5)
#                 if len(set(l))<15:
#                     continue

#                 print("Sol: ", l)

# print('done')

#other stuff below
count = 0
for a in range(1,16):
    for b in range(1,a+1):
        for c in range(1,b+1):
            for d in range(1,c+1):
                for e in range(1,d+1):
                    if a+b+c+d+e==a*b*c*d*e:
                        count+=1
                        print(a,b,c,d,e)
    
