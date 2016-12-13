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


service_time = get_next([(1, 0.1), (2, 0.2), (3, 0.3), (4, 0.25), (5, 0.1), (6, 0.05)], 2)
arrival_time = get_next([(1, 0.125), (2, 0.125), (3, 0.125), (4, 0.125), (5, 0.125), (6, 0.125), (7, 0.125), (8, 0.125)]
                        , 3)
print(
    'Customer	Inter-arrival time	Clock	Service time	Start time	End time	Queue waiting time	Total time	Server idle time')

cust = 0
inter_arrival = 1
clock = 2
serv_time = 3
start_time = 4
end_time = 5
queue_time = 6
total_time = 7
idle_time = 8

rows = []
row = [0 for i in range(9)]
row[cust] = 1
row[inter_arrival] = 0
row[clock] = 0
row[serv_time] = next(service_time)
row[start_time] = 0
row[end_time] = row[serv_time]
row[queue_time] = row[start_time] - row[clock]
row[total_time] = row[end_time] - row[start_time]
row[idle_time] = 0

rows.append(row)
print('\t'.join(map(lambda x: str(x), row)))

for j in range(20):
    row = [0 for k in range(9)]
    row[cust] = rows[-1][cust] + 1
    row[inter_arrival] = next(arrival_time)
    row[clock] = rows[-1][clock] + row[inter_arrival]
    row[serv_time] = next(service_time)
    row[start_time] = max(rows[-1][end_time], row[clock])
    row[end_time] = row[start_time] + row[serv_time]
    row[queue_time] = row[start_time] - row[clock]
    row[total_time] = row[end_time] - row[start_time]
    row[idle_time] = row[start_time] - rows[-1][end_time]
    rows.append(row)
    print('\t'.join(map(lambda x: str(x), row)))
