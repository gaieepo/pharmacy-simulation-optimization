from costf import costfunction
from config import *


def find_single_neighbors(sche):
    assert sum(sche) == NUM_PHAR
    res = []
    for i in range(len(sche) - 1):
        for j in range(i + 1, len(sche)):
            if sche[i] < NUM_PHAR - len(sche) + 1 and sche[j] > 1:
                res.append(sche[:i] + [sche[i] + 1] +
                           sche[i + 1:j] + [sche[j] - 1] + sche[j + 1:])
            if sche[i] > 1 and sche[j] < NUM_PHAR - len(sche) + 1:
                res.append(sche[:i] + [sche[i] - 1] +
                           sche[i + 1:j] + [sche[j] + 1] + sche[j + 1:])
    return res


def find_neighbors(sche):
    assert len(sche[0]) == 5
    res = []
    for i in range(len(sche)):
        single_neighbors = find_single_neighbors(sche[i])
        for j in range(len(single_neighbors)):
            res.append(sche[:i] + [single_neighbors[j]] + sche[i + 1:])
    return res


def hillclimb(init=None):
    assert len(init) == NUM_HOUR
    sche = init
    while True:
        neighbors = find_neighbors(sche)
        current = costfunction(sche)
        print(sche, current)
        best = current
        for i in range(len(neighbors)):
            cost = costfunction(neighbors[i])
            if cost < best:
                best = cost
                sche = neighbors[i]
        if current == best:
            break
    return [sche, current]


def output_to_file():
    result = hillclimb(INIT_SCHEDULE)
    with open('output.log', 'a') as outfile:
        outfile.write(str(NUM_PHAR) + ' ' + str(ITERATIONS) +
                      ' ' + str(result[1]) + ' ' + str(result[0]) + '\n')

output_to_file()
