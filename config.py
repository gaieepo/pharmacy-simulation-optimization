ITERATIONS = 10
NUM_PHAR = 11
SEED = 42

DEBUG = True
MAX_PHAR_NUM = NUM_PHAR - 4
SIM_HOUR = 3600
NUM_HOUR = 9
BASE_INTERVAL = 60
SIM_TIME = SIM_HOUR * NUM_HOUR

INTERVAL_ARGS = [
    0.00798,
    0.01122,
    0.01190,
    0.01047,
    0.00621,
    0.00724,
    0.01127,
    0.01054,
    0.00740
]

# require SIM_TIME to be SIM_HOUR * 2
SAMPLE_SCHEDULE = [
    [1, 1, 1, 1, 1],
    [7, 7, 7, 7, 7]
]

INIT_SCHEDULE_PLAN = [
    [MAX_PHAR_NUM, 1, 1, 1, 1],
    [MAX_PHAR_NUM, 1, 1, 1, 1],
    [MAX_PHAR_NUM, 1, 1, 1, 1],
    [MAX_PHAR_NUM, 1, 1, 1, 1],
    [MAX_PHAR_NUM, 1, 1, 1, 1],
    [MAX_PHAR_NUM, 1, 1, 1, 1],
    [MAX_PHAR_NUM, 1, 1, 1, 1],
    [MAX_PHAR_NUM, 1, 1, 1, 1],
    [MAX_PHAR_NUM, 1, 1, 1, 1]
]

BEST_SCHEDULE_PLAN = [
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
