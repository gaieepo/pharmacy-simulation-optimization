ITERATIONS = 10
NUM_PHAR = 11

DEBUG = False
MAX_PHAR = NUM_PHAR - 4
SIM_HOUR = 3600
NUM_HOUR = 9
SIM_TIME = SIM_HOUR * NUM_HOUR

# require SIM_TIME to be SIM_HOUR * 2
SAMPLE_SCHEDULE = [
    [1, 1, 1, 1, 1],
    [7, 7, 7, 7, 7]
]

INIT_SCHEDULE = [
    [MAX_PHAR, 1, 1, 1, 1],
    [MAX_PHAR, 1, 1, 1, 1],
    [MAX_PHAR, 1, 1, 1, 1],
    [MAX_PHAR, 1, 1, 1, 1],
    [MAX_PHAR, 1, 1, 1, 1],
    [MAX_PHAR, 1, 1, 1, 1],
    [MAX_PHAR, 1, 1, 1, 1],
    [MAX_PHAR, 1, 1, 1, 1],
    [MAX_PHAR, 1, 1, 1, 1]
]

BEST_SCHEDULE = [
    [3, 2, 2, 3, 1],
    [3, 2, 2, 3, 1],
    [3, 2, 2, 3, 1],
    [3, 2, 2, 3, 1],
    [3, 2, 2, 3, 1],
    [3, 3, 2, 2, 1],
    [3, 3, 1, 3, 1],
    [3, 2, 2, 3, 1],
    [3, 2, 2, 3, 1]
]
