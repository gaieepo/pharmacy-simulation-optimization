"""
pharmacy simulation cost function environment

Assumptions:
- Station numbers are stable: registration, packing, checking, dispensing, payment

Variables:
- Total number of pharmacists
- Working time
- Schedule

TODO:
- Distinguish pharmacists and technicians
- GUI
- Logging time returned coupling (remove mysterious numbers)

"""
import simpy
import random
import itertools
from config import *


#########################################################
# utils
#########################################################
def is_all_done(*booths):
    for booth in booths:
        if not booth.is_done:
            return False
    return True


def log_it(text):
    if DEBUG:
        print(text)


def logging(data):
    if DEBUG:
        for k, v in data.items():
            print("{}\n"
                  "queue reg {:.1f} [{:.1f}, {:.1f}] reg {:.1f} [{:.1f}, {:.1f}]\n"
                  "queue pac {:.1f} [{:.1f}, {:.1f}] pac {:.1f} [{:.1f}, {:.1f}]\n"
                  "queue che {:.1f} [{:.1f}, {:.1f}] che {:.1f} [{:.1f}, {:.1f}]\n"
                  "queue dis {:.1f} [{:.1f}, {:.1f}] dis {:.1f} [{:.1f}, {:.1f}]\n"
                  "queue pay {:.1f} [{:.1f}, {:.1f}] pay {:.1f} [{:.1f}, {:.1f}]\n"
                  "total {:.1f}\n"
                  .format(k,
                          v[1]-v[0], v[0], v[1], v[2]-v[1], v[1], v[2],
                          v[3]-v[2], v[2], v[3], v[4]-v[3], v[3], v[4],
                          v[5]-v[4], v[4], v[5], v[6]-v[5], v[5], v[6],
                          v[7]-v[6], v[6], v[7], v[8]-v[7], v[7], v[8],
                          v[9]-v[8], v[8], v[9], v[10]-v[9], v[9], v[10],
                          v[10]-v[0])
                  )


def evaluate(data):
    """ Cost function evaluation parameters:
        - average_total_time
        - average_total_queue_time
        - average_utility_rate (inverse relationship)
    """
    average_total_time = sum(v[10] - v[0]
                             for v in data.values()) / len(data.values())
    average_total_queue_time = sum(
        sum(v[1::2]) - sum(v[:-1:2]) for v in data.values()) / len(data.values())
    return average_total_time + average_total_queue_time


#########################################################
# simulation
#########################################################
class Booth(simpy.PriorityResource):
    @property
    def is_done(self):
        return len(self.queue) == 0 and len(self.users) == 0


def patient(name, env, data, generation_terminate, reg_booth, pac_booth, che_booth, dis_booth, pay_booth):
    data.setdefault(name, [])
    log_it(f"{name} arrives at {env.now:.1f}")
    with reg_booth.request() as reg_req:
        data[name].append(env.now)
        log_it(f"{name} queues reg at {env.now:.1f}")
        yield reg_req
        log_it(f"{name} starts reg at {env.now:.1f}")
        data[name].append(env.now)
        yield env.timeout(random.uniform(30, 300))
        log_it(f"{name} finishes reg at {env.now:.1f}")
    with pac_booth.request() as pac_req:
        data[name].append(env.now)
        log_it(f"{name} queues pac at {env.now:.1f}")
        yield pac_req
        log_it(f"{name} starts pac at {env.now:.1f}")
        data[name].append(env.now)
        yield env.timeout(random.uniform(120, 480))
        log_it(f"{name} finishes pac at {env.now:.1f}")
    with che_booth.request() as che_req:
        data[name].append(env.now)
        log_it(f"{name} queues che at {env.now:.1f}")
        yield che_req
        log_it(f"{name} starts che at {env.now:.1f}")
        data[name].append(env.now)
        yield env.timeout(random.uniform(10, 300))
        log_it(f"{name} finishes che at {env.now:.1f}")
    with dis_booth.request() as dis_req:
        data[name].append(env.now)
        log_it(f"{name} queues dis at {env.now:.1f}")
        yield dis_req
        log_it(f"{name} starts dis at {env.now:.1f}")
        data[name].append(env.now)
        yield env.timeout(random.uniform(60, 600))
        log_it(f"{name} finishes dis at {env.now:.1f}")
    with pay_booth.request() as pay_req:
        data[name].append(env.now)
        log_it(f"{name} queues pay at {env.now:.1f}")
        yield pay_req
        log_it(f"{name} starts pay at {env.now:.1f}")
        data[name].append(env.now)
        yield env.timeout(random.uniform(30, 180))
        log_it(f"{name} finishes pay at {env.now:.1f}")
    data[name].append(env.now)
    log_it(f"{name} leaves at {env.now:.1f}")
    if env.now > SIM_TIME and is_all_done(reg_booth, pac_booth, che_booth, dis_booth, pay_booth):
        generation_terminate.succeed()


def calculate_break(sche):
    assert len(sche) > 0
    res = []
    for i in range(len(sche[0])):
        station_res = [[] for phar in range(MAX_PHAR_NUM)]
        station = [s[i] for s in sche]
        prev = MAX_PHAR_NUM
        for t in range(len(sche)):
            if station[t] < prev:
                for k in range(station[t], prev):
                    station_res[k].append(t)
            elif station[t] > prev:
                for k in range(prev, station[t]):
                    station_res[k].append(t)
            prev = station[t]
        for k in range(prev, MAX_PHAR_NUM):
            station_res[k].append(len(sche))
        res.append(station_res)
    return res


def create_break(env, phar, timings):
    assert len(timings) % 2 == 0
    prev = 0
    for t in range(0, len(timings), 2):
        env.timeout(timings[t] * SIM_HOUR - prev)
        with phar.request(priority=-1) as req:
            yield req
            yield env.timeout((timings[t+1] - timings[t]) * SIM_HOUR)


def schedule_break(env, schedule, reg_booth, pac_booth, che_booth, dis_booth, pay_booth):
    break_schedule = calculate_break(schedule)
    reg, pac, che, dis, pay = break_schedule
    for i in reg:
        if i:
            env.process(create_break(env, reg_booth, i))
    for i in pac:
        if i:
            env.process(create_break(env, pac_booth, i))
    for i in che:
        if i:
            env.process(create_break(env, che_booth, i))
    for i in dis:
        if i:
            env.process(create_break(env, dis_booth, i))
    for i in pay:
        if i:
            env.process(create_break(env, pay_booth, i))


def patient_generator(env, data, generation_terminate, reg_booth, pac_booth, che_booth, dis_booth, pay_booth):
    total_time = 0
    for i in itertools.count():
        env.process(patient('Patient %d' % i, env, data, generation_terminate, reg_booth,
                            pac_booth, che_booth, dis_booth, pay_booth))
        random_interval = random.expovariate(INTERVAL_ARGS[int(total_time//SIM_HOUR)])
        interval = random_interval + BASE_INTERVAL
        total_time += interval
        if total_time > SIM_TIME:
            break
        yield env.timeout(interval)
    yield generation_terminate


def simulate(schedule_plan, seed=SEED):

    # universal random seed
    random.seed(seed)

    # initialize simulation env
    env = simpy.Environment()

    reg_booth = Booth(env, capacity=MAX_PHAR_NUM)
    pac_booth = Booth(env, capacity=MAX_PHAR_NUM)
    che_booth = Booth(env, capacity=MAX_PHAR_NUM)
    dis_booth = Booth(env, capacity=MAX_PHAR_NUM)
    pay_booth = Booth(env, capacity=MAX_PHAR_NUM)

    data = {}

    generation_terminate = env.event()

    schedule_break(env, schedule_plan,
                   reg_booth, pac_booth, che_booth, dis_booth, pay_booth)

    patient_gen_process = env.process(
        patient_generator(env, data, generation_terminate,
                          reg_booth, pac_booth, che_booth, dis_booth, pay_booth))

    env.run(until=patient_gen_process)

    logging(data)

    return evaluate(data)


def calculate_cost(schedule_plan, iterations=ITERATIONS):
    """ simulation cost calculation

    Calculate average cost over number iterations of simulation run

    Args:
        iteration (int): number of iteration to prevent lucky collision
    """
    total_cost = 0

    for i in range(iterations):
        total_cost += simulate(schedule_plan=schedule_plan, seed=i)

    cost = total_cost / iterations
    return cost


if __name__ == '__main__':
    # print(calculate_cost(INIT_SCHEDULE_PLAN))
    print(simulate(INIT_SCHEDULE_PLAN))
