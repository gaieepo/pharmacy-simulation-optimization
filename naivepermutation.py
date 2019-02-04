from costf import calculate_cost


def schedule_permutation(num_phar):
    for i in range(1, num_phar - 4 + 1):
        for j in range(1, num_phar - i - 3 + 1):
            for k in range(1, num_phar - i - j - 2 + 1):
                for l in range(1, num_phar - i - j - k - 1 + 1):
                    m = num_phar - i - j - k - l
                    yield [i, j, k, l, m]


def naivepermutation():
    best = float('inf')
    for i in schedule_permutation(11):
        cost = calculate_cost(i)
        if cost < best:
            best = cost
            print(i, cost)
