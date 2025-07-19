from random import randint

final_money = []
for _ in range(1000000):
    money = 2
    while True:
        roll = randint(1,4)
        if roll == 1:
            final_money.append(money/2)
            break
        elif roll == 2:
            money = money/2 + 2
        else:
            money+=2

print(sum(final_money)/len(final_money))
        