ans = 0
x = set()
y = set()
for i in range(1024):
    num = i
    string = "aaaaaaaaaa"
    for j in range(10):
        if num % (2 ** (j + 1)):
            string = string[0:j] + "b" + string[j + 1 :]
            num -= num % (2 ** (j + 1))
    x.add(string)
    # print(string)
    if string.find("aaaa") == -1 and string.find("bbbb") == -1:
        y.add(string)
        ans += 1
print(y)
print(ans)
