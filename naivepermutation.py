from costf import costfunction


def naivepermutation(n):
    for i in range(1, n - 4 + 1):
        for j in range(1, n - i - 3 + 1):
            for k in range(1, n - i - j - 2 + 1):
                for l in range(1, n - i - j - k - 1 + 1):
                    m = n - i - j - k - l
                    yield [i, j, k, l, m]

best = float('inf')
for i in naivepermutation(11):
    cost = costfunction(i)
    if cost < best:
        best = cost
        print(i, cost)
