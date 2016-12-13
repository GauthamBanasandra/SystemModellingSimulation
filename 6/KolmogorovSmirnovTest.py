import random

n = 20
numbers = sorted([random.randint(1, 100) for i in range(n)])
d_plus = max([(i[0] + 1) / n - i[1] for i in enumerate(numbers)])
d_minus = max([i[1] - i[0] / n for i in enumerate(numbers)])
d = max(d_plus, d_minus)
print(numbers)
print(d_plus, d_minus, d)
