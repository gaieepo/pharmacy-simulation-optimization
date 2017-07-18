from costf import costfunction


def find_neighbors(sche, n):
    if sum(sche) != n:
        return None
    res = []
    for i in range(len(sche) - 1):
        for j in range(i + 1, len(sche)):
            if sche[i] < n - len(sche) + 1 and sche[j] > 1:
                res.append(sche[:i] + [sche[i] + 1] +
                           sche[i + 1:j] + [sche[j] - 1] + sche[j + 1:])
            if sche[i] > 1 and sche[j] < n - len(sche) + 1:
                res.append(sche[:i] + [sche[i] - 1] +
                           sche[i + 1:j] + [sche[j] + 1] + sche[j + 1:])
    return res


def hillclimb(n, init=[1, 1, 1, 1, 7]):
    sche = init
    while True:
        neighbors = find_neighbors(sche, n)
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
    return sche

print('Result: ', hillclimb(11))
