import random


def get_ranges(_n, _k):
    ivt = _k / _n
    _ranges = [(0, round(ivt, 2))]
    for i in range(1, _n // _k):
        _ranges.append((round(ivt * i, 1), round(ivt * (i + 1), 1)))
    return _ranges


def get_freq(r, _numbers):
    count = 0
    for i in _numbers:
        if r[0] <= i < r[1]:
            count += 1
    return count


n = 100
k = 10
exp_freq = n / k
numbers = sorted([random.random() for i in range(n)])
ranges = get_ranges(n, k)
obs_freq = [get_freq(r, numbers) for r in ranges]
chi_sq = [((o - exp_freq) ** 2) / exp_freq for o in obs_freq]
print('range\tobs freq\texp freq\tchi sq')
for j in range(len(ranges)):
    print(ranges[j], obs_freq[j], exp_freq, chi_sq[j], sep='\t')
print('\t\t\t', sum(chi_sq))
