def fibonacci(n):
    if n <= 0:
        return 0
    elif n == 1:
        return 1

    # Initialize base cases
    fib = [0] * (n + 1)
    fib[1] = 1

    # Fill the array using the bottom-up approach
    for i in range(2, n + 1):
        fib[i] = fib[i - 1] + fib[i - 2]

    return fib[n]

# Example usage
n = 1000
print(f"The {n}th Fibonacci number is: {fibonacci(n)}")
