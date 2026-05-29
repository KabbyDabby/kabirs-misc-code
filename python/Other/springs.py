springs = [5.767, 2.878, 6.507, 5.829, 6.751]

possible_consants = {}
for i in range(len(springs)):
    for j in range(i + 1, len(springs)):
        possible_consants[(springs[i], springs[j], 0)] = springs[i] + springs[j]
        possible_consants[(springs[i], springs[j], 1)] = 1 / (
            1 / springs[i] + 1 / springs[j]
        )

for key in sorted(possible_consants):
    print(key, possible_consants[key])
