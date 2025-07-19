
def problem(max):
    prev = 1
    current = 1
    total = 0

    while current < max:
        temp = current
        current += prev
        prev = temp

        if current % 2 == 0:
            total += current

    if current % 2 == 0:
        total -= current
    
    print(total)
    

problem(4000000)