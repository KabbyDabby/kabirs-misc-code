#999*889<900000
#we want 9abba9
#we have that our two numbers are 9xy *9rs
#y,s = 1,9 or 3,3
ans = set()
#1,9 case
for i in range(10):
    for j in range(10):
        a = 901+10*i
        b = 909+10*j
        prod = a*b
        if str(prod)[:3] == str(prod)[3:][::-1]:
            ans.add(prod)

#3,3, case
for i in range(10):
    for j in range(i,10):
        a = 903+10*i
        b = 903+10*j
        prod = a*b
        if str(prod)[:3] == str(prod)[3:][::-1]:
            ans.add(prod)

print(max(ans))

