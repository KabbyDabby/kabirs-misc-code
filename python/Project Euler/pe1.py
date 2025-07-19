def problem(max):
    total = 0
    for i in range(1,max):
        if i % 15 == 0:
            total -= i
        
        if i%5 == 0:
            total +=i
        
        if i%3 == 0:
            total +=i

    print(total)

problem(1000)