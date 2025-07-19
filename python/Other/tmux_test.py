# Print every 10th Fibonacci number from 0 to 100
fib_sequence = [0, 1]
while len(fib_sequence) < 100:
    fib_sequence.append(fib_sequence[-1] + fib_sequence[-2])

# Print every 10th Fibonacci number (0-indexed)
for i in range(9, len(fib_sequence), 10):
    print(fib_sequence[i])
