import time
import math

def slow_loop(n):
    total = 0
    for i in range(1, n):
        # Intentionally heavy operation: factorial
        total += math.factorial(i % 20)  # limit input to avoid math range error
    return total

n = 100000000000
start = time.time()
result = slow_loop(n)
end = time.time()

print(f"[Python] Result: {result}")
print(f"[Python] Time taken: {end - start:.4f} seconds")