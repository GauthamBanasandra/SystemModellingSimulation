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
                yield rand_int


arrival_time = get_next([(1, 0.25), (2, 0.4), (3, 0.2), (4, 0.15)], 2)
service_time_able = get_next([(2, 0.3), (3, 0.28), (4, 0.25), (5, 0.17)], 2)
service_time_baker = get_next([(3, 0.35), (4, 0.25), (5, 0.2), (6, 0.2)], 2)

print(
    'Customer	Inter-arrival time	Clock	Service time(Able)	Start time(Able)	End time(Able)	Service time(Baker)	Start time(Baker)	End time(Baker)	Queue time')

cust = 0
inter_arrival = 1
clock = 2
serv_time_able = 3
start_time_able = 4
end_time_able = 5
serv_time_baker = 6
start_time_baker = 7
end_time_baker = 8
queue_time = 9

rows = []
row = [0 for i in range(10)]
row[cust] = 1
row[inter_arrival] = 0
row[clock] = 0
row[serv_time_able] = next(service_time_able)
row[start_time_able] = 0
row[end_time_able] = row[serv_time_able]
row[serv_time_baker] = '-'
row[start_time_baker] = '-'
row[end_time_baker] = '-'
row[queue_time] = 0

rows.append(row)
print('\t'.join(map(lambda x: str(x), row)))


def get_time(idx):
    return rows[-1][idx] if rows[-1][idx] != '-'else 0

# Simulating for 20 customers.
while True:
    row = [0 for k in range(10)]
    row[cust] = rows[-1][cust] + 1
    row[inter_arrival] = next(arrival_time)
    row[clock] = rows[-1][clock] + row[inter_arrival]
    # Decide the server.
    # If Able is going to be free sooner than Baker.
    if max(row[clock], get_time(end_time_able)) < max(row[clock], get_time(end_time_baker)):
        row[serv_time_able] = next(service_time_able)
        row[start_time_able] = rows[-1][end_time_able]
        row[end_time_able] = row[clock] + row[serv_time_able]
        row[serv_time_baker] = '-'
        row[start_time_baker] = '-'
        row[end_time_baker] = '-'
        row[queue_time] = row[end_time_able] - row[clock]
    else:  # Baker is going to be free sooner than Able.
        row[serv_time_baker] = next(service_time_baker)
        row[start_time_baker] = get_time(end_time_baker)
        row[end_time_baker] = row[clock] + row[serv_time_baker]
        row[serv_time_able] = '-'
        row[start_time_able] = '-'
        row[end_time_able] = '-'
        row[queue_time] = row[end_time_baker] - row[clock]

    print('\t'.join(map(lambda x: str(x), row)))
    rows.append(row)
    if row[cust] > 20:
        break
