residues = {' ':' '}
chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
for i in range(26):
    residues[chars[i]] = chr((i**11)%26+ord('A'))
i
# print(residues)
def encode(s):
    # print(s)
    # print([residues[c.upper()] for c in s])
    return ''.join([residues[c.upper()] for c in s])


print(encode("Mr Pisani should contact Spencer Teoft"))

decoder = {v: k for k, v in residues.items()}
def decode(s):
    return ''.join([decoder[c] for c in s])

print(decode(encode("Mr Pisani should contact Spencer Teoft")))