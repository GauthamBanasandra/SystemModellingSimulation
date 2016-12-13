import math
import random


# Yields the next arrival or service times.
def get_next(data, digits):
    """
    :param digits: digits to be rounded off.
    :param data: list of (service_time, probability).
    :return: next arrival/service time.
    """
    if sum(map(lambda x: x[1], data)) != 1:
        raise Exception('invalid probabilities')
    service_time = list(map(lambda x: x[0], data))
    cuml_prob = [data[0][1]]
    for i in range(1, len(data)):
        cuml_prob.append(math.floor((cuml_prob[i - 1] + data[i][1]) * (10 ** digits)) / (10 ** digits))
    cuml_prob = [0] + list(map(lambda x: int(x * 10 ** digits), cuml_prob))
    ranges = {range(cuml_prob[i] + 1, cuml_prob[i + 1]): service_time[i] for i in range(len(cuml_prob) - 1)}
    while True:
        rand_int = int(random.random() * 10 ** digits)
        for k in ranges.keys():
            if rand_int in k:
                yield ranges[k]


def get_demand(d_type):
    if d_type == 'good':
        return next(demand_good)
    elif d_type == 'fair':
        return next(demand_fair)
    elif d_type == 'poor':
        return next(demand_poor)


day_type = get_next([('good', 0.35), ('fair', 0.45), ('poor', 0.2)], 2)
demand_good = get_next([(40, 0.03), (50, 0.05), (60, 0.15), (70, 0.2), (80, 0.35), (90, 0.15), (100, 0.07)], 2)
demand_fair = get_next([(40, 0.10), (50, 0.18), (60, 0.40), (70, 0.2), (80, 0.08), (90, 0.04), (100, 0.00)], 2)
demand_poor = get_next([(40, 0.44), (50, 0.22), (60, 0.16), (70, 0.12), (80, 0.06), (90, 0.00), (100, 0.00)], 2)

print('Day	Day type	Demand	Revenue	Lost profit	Salvage	Profit')

_day = 0
_day_type = 1
_demand = 2
_revenue = 3
_lost_profit = 4
_salvage = 5
_profit = 6

num_newspapers = 7 * 10

for j in range(20):
    row = [0 for i in range(7)]
    row[_day] = j + 1
    row[_day_type] = next(day_type)
    row[_demand] = get_demand(row[_day_type])
    if num_newspapers > row[_demand]:
        row[_revenue] = row[_demand] * 0.5
        row[_lost_profit] = 0
        row[_salvage] = (num_newspapers - row[_demand]) * 0.05
    else:
        row[_revenue] = num_newspapers * 0.5
        row[_lost_profit] = (row[_demand] - num_newspapers) * (0.5 - 0.33)
        row[_salvage] = 0
    row[_profit] = row[_revenue] - num_newspapers * 0.33 + row[_salvage] - row[_lost_profit]
    print('\t'.join(map(lambda x: str(x), row)))
