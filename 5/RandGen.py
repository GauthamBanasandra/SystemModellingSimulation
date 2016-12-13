import math


def rand(a, x, c, m, n):
    for i in range(n):
        x = (a * x + c) % m
        yield x


def is_prime(k):
    if k == 0 or k == 1:
        return False
    for i in range(2, k):
        if k % i == 0:
            return False
    return True


def is_two_pow(k):
    t = 2
    while t <= k:
        if t == k:
            return True
        t *= 2
    return False


def longest_cycle(a, x0, c, m):
    if c != 0 and is_two_pow(m) and math.gcd(c, m) == 1 and (a - 1) / 4 == math.floor((a - 1) / 4):
        return m
    if c == 0 and is_two_pow(m) and x0 % 2 != 0 and (
                        (a - 3) / 8 == math.floor((a - 3) / 8) or (a - 3) / 8 == math.floor((a - 3))):
        return m // 4
    if c == 0 and is_prime(m) and (a ** (m - 1) - 1) / m == math.floor((a ** (m - 1) - 1) / m):
        return (m - 1) // 2


a = 17
x = 27
c = 7
m = 16
print('longest cycle:', longest_cycle(a, x, c, m))
rand_nums = set()
for i in rand(a, x, c, m, 16):
    rand_nums.add(i)
print('count=', len(rand_nums), rand_nums)
