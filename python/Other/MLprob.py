
num_cases = int ((15 * 14 * 13)/6)
total_24 = 0
total = 0
for i in range(1,14):
    for j in range(i+1, 15):
        for k in range (j+1, 16):
            if i + j + k <= 24:
                total += 1
            if i + j + k == 24:
                total_24 += 1
                

print(total)

print(int((num_cases-total_24)/2+total_24))
print(num_cases)




