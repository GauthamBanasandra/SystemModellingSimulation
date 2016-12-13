import math
import random


# Yields the next arrival or service times.
def get_next(data, digits):
    """
    :param digits: digits to be rounded off.
    :param data: list of (service_time, probability).
    :return: next arrival/service time.
    """
    # if sum(map(lambda x: x[1], data)) != 1:
    #     raise Exception('invalid probabilities')
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


demand = get_next([(0, 0.1), (1, 0.25), (2, 0.35), (3, 0.21), (4, 0.09)], 2)
lead_time = get_next([(1, 0.6), (2, 0.3), (3, 0.1)], 2)

print(
    'Cycle	Day	Beginning inventory	Demand	Ending inventory	Shortage qty	Order qty	Order arrives in')

_cycle = 0
_day = 1
_start_ivt = 2
_demand = 3
_end_ivt = 4
_shortage = 5
_order = 6
_arrives_in = 7

row = [0 for i in range(8)]
row[_cycle] = 1
row[_day] = 1
row[_start_ivt] = 3
row[_demand] = next(demand)
if row[_start_ivt] >= row[_demand]:
    row[_end_ivt] = row[_start_ivt] - row[_demand]
    row[_order] = row[_shortage] = 0
else:
    row[_end_ivt] = row[_start_ivt]
    row[_order] = row[_shortage] = row[_demand] - row[_start_ivt]
row[_arrives_in] = 1

order_arrived = False
order_set = False
order_qty = 8

print('\t'.join(map(lambda x: str(x), row)))
rows = [row]

for k in range(1, 26):
    row = [0 for j in range(8)]
    row[_cycle] = k // 5 + 1
    row[_day] = k % 5 + 1
    if rows[-1][_arrives_in] != '-':
        if rows[-1][_arrives_in] > 0:
            row[_arrives_in] = rows[-1][_arrives_in] - 1
        elif rows[-1][_arrives_in] == 0:
            order_arrived = True
            row[_arrives_in] = '-'
    else:
        row[_arrives_in] = '-'
    if order_arrived:
        row[_start_ivt] = rows[-1][_end_ivt] + order_qty
        if row[_start_ivt] > row[_order]:
            row[_start_ivt] -= row[_order]
            row[_order] = 0
        else:
            row[_start_ivt] = 0
            row[_order] -= row[_start_ivt]
        order_arrived = False
    else:
        row[_start_ivt] = rows[-1][_end_ivt]
    row[_demand] = next(demand)
    if row[_start_ivt] >= row[_demand]:
        row[_end_ivt] = row[_start_ivt] - row[_demand]
        row[_shortage] = 0
        row[_order] = rows[-1][_order]
    else:
        row[_end_ivt] = row[_start_ivt]
        row[_shortage] = row[_demand] - row[_start_ivt]
        row[_order] = rows[-1][_order] + row[_shortage]
    if order_set:
        row[_arrives_in] = next(lead_time) - 1
        order_set = False
    if row[_day] == 5:
        order_qty = row[_order] if row[_order] > 0 else 13 - row[_start_ivt]
        order_set = True
    rows.append(row)
    print('\t'.join(map(lambda x: str(x), row)))

    # 9448382108
# 8050579670