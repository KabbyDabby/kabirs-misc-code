digits = [2,3,5,7]
for a in digits:
    for b in digits:
        for c in digits:
            for d in digits:
                for e in digits:
                    first = (100*a+10*b+c)*e
                    if first//1000==0:
                        continue
                    
                    second = (100*a+10*b+c)*d

                    # print(second)

                    if second//1000 == 0:
                        continue

                    res = (100*a+10*b+c)*(10*d+e)
                    if res//10000==0:
                        continue
                    for f in str(first):
                        if int(f) not in digits:
                            break
                    else:
                        for dd in str(second):
                            if int(dd) not in digits:
                                break
                        else:
                            for digit in str(res):
                                if int(digit) not in digits:
                                    break
                            else:
                                print(f'  {100*a+10*b+c}')
                                print(f'   {10*d+e}')
                                print('-----')
                                print(f' {first}')
                                print(second)
                                print('-----')
                                print(res)