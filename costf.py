import simpy
import random
import itertools
from config import *

NUM_PHAR = 3
SIM_HOUR = 3600
SIM_TIME = SIM_HOUR * 9


class Phar(simpy.Resource):
    def is_done(self):
        return len(self.queue) == 0 and len(self.users) == 0


def patient(name, env, data, generation_terminate, reg_phar, pac_phar, che_phar, dis_phar, pay_phar):
    data.setdefault(name, [])
    # print('%s arrives at %.1f' % (name, env.now))
    with reg_phar.request() as reg_req:
        data[name].append(env.now)
        # print('%s queues reg at %.1f' % (name, env.now))
        yield reg_req
        # print('%s starts reg at %.1f' % (name, env.now))
        data[name].append(env.now)
        yield env.timeout(random.uniform(30, 300))
        # print('%s finishes reg at %.1f' % (name, env.now))
    with pac_phar.request() as pac_req:
        data[name].append(env.now)
        # print('%s queues pac at %.1f' % (name, env.now))
        yield pac_req
        # print('%s starts pac at %.1f' % (name, env.now))
        data[name].append(env.now)
        yield env.timeout(random.uniform(120, 480))
        # print('%s finishes pac at %.1f' % (name, env.now))
    with che_phar.request() as che_req:
        data[name].append(env.now)
        # print('%s queues che at %.1f' % (name, env.now))
        yield che_req
        # print('%s starts che at %.1f' % (name, env.now))
        data[name].append(env.now)
        yield env.timeout(random.uniform(10, 300))
        # print('%s finishes che at %.1f' % (name, env.now))
    with dis_phar.request() as dis_req:
        data[name].append(env.now)
        # print('%s queues dis at %.1f' % (name, env.now))
        yield dis_req
        # print('%s starts dis at %.1f' % (name, env.now))
        data[name].append(env.now)
        yield env.timeout(random.uniform(60, 600))
        # print('%s finishes dis at %.1f' % (name, env.now))
    with pay_phar.request() as pay_req:
        data[name].append(env.now)
        # print('%s queues pay at %.1f' % (name, env.now))
        yield pay_req
        # print('%s starts pay at %.1f' % (name, env.now))
        data[name].append(env.now)
        yield env.timeout(random.uniform(30, 180))
        # print('%s finishes pay at %.1f' % (name, env.now))
    data[name].append(env.now)
    # print('%s leaves at %.1f' % (name, env.now))
    if env.now > SIM_TIME and is_all_done(reg_phar, pac_phar, che_phar, dis_phar, pay_phar):
        generation_terminate.succeed()


def is_all_done(*args):
    for arg in args:
        if not arg.is_done():
            return False
    return True


def logging(data):
    for k, v in data.items():
        print('''
%s:
queue reg %.1f [%.1f, %.1f] reg %.1f [%.1f, %.1f],
queue pac %.1f [%.1f, %.1f] pac %.1f [%.1f, %.1f],
queue che %.1f [%.1f, %.1f] che %.1f [%.1f, %.1f],
queue dis %.1f [%.1f, %.1f] dis %.1f [%.1f, %.1f],
queue pay %.1f [%.1f, %.1f] pay %.1f [%.1f, %.1f],
total %.1f
            ''' % (k, v[1] - v[0], v[0], v[1], v[2] - v[1], v[1], v[2],
                   v[3] - v[2], v[2], v[3], v[4] - v[3], v[3], v[4],
                   v[5] - v[4], v[4], v[5], v[6] - v[5], v[5], v[6],
                   v[7] - v[6], v[6], v[7], v[8] - v[7], v[7], v[8],
                   v[9] - v[8], v[8], v[9], v[10] - v[9], v[9], v[10],
                   v[10] - v[0]))


def evaluate(data):
    """
    Cost function evaluation parameters:
        - average_total_time
        - average_total_queue_time
        - average_utility_rate
    """
    average_total_time = sum(v[10] - v[0]
                             for v in data.values()) / len(data.values())
    average_total_queue_time = sum(
        sum(v[1::2]) - sum(v[:-1:2]) for v in data.values()) / len(data.values())
    return average_total_time + average_total_queue_time


def patient_generator(env, data, generation_terminate, reg_phar, pac_phar, che_phar, dis_phar, pay_phar):
    total_time = 0
    for i in itertools.count():
        env.process(patient('Patient %d' % i, env, data, generation_terminate, reg_phar,
                            pac_phar, che_phar, dis_phar, pay_phar))
        base_interval = 0
        if SIM_HOUR * 0 <= total_time < SIM_HOUR * 1:
            base_interval = random.expovariate(0.00798)
        elif SIM_HOUR * 1 <= total_time < SIM_HOUR * 2:
            base_interval = random.expovariate(0.01122)
        elif SIM_HOUR * 2 <= total_time < SIM_HOUR * 3:
            base_interval = random.expovariate(0.01190)
        elif SIM_HOUR * 3 <= total_time < SIM_HOUR * 4:
            base_interval = random.expovariate(0.01047)
        elif SIM_HOUR * 4 <= total_time < SIM_HOUR * 5:
            base_interval = random.expovariate(0.00621)
        elif SIM_HOUR * 5 <= total_time < SIM_HOUR * 6:
            base_interval = random.expovariate(0.00724)
        elif SIM_HOUR * 6 <= total_time < SIM_HOUR * 7:
            base_interval = random.expovariate(0.01127)
        elif SIM_HOUR * 7 <= total_time < SIM_HOUR * 8:
            base_interval = random.expovariate(0.01054)
        elif SIM_HOUR * 8 <= total_time < SIM_HOUR * 9:
            base_interval = random.expovariate(0.00740)
        interval = base_interval + 60
        total_time += interval
        if total_time > SIM_TIME:
            break
        yield env.timeout(interval)
    yield generation_terminate


def simulate(schedule, seed):
    random.seed(seed)
    env = simpy.Environment()
    reg_phar = Phar(env, capacity=schedule[0])
    pac_phar = Phar(env, capacity=schedule[1])
    che_phar = Phar(env, capacity=schedule[2])
    dis_phar = Phar(env, capacity=schedule[3])
    pay_phar = Phar(env, capacity=schedule[4])
    data = {}
    generation_terminate = env.event()
    p = env.process(patient_generator(env, data, generation_terminate, reg_phar,
                                      pac_phar, che_phar, dis_phar, pay_phar))
    env.run(until=p)
    if DEBUG:
        logging(data)
    return evaluate(data)


def costfunction(schedule=[10, 10, 10, 10, 10], iterations=10):
    total_cost = 0
    for i in range(iterations):
        total_cost += simulate(schedule=schedule, seed=i)
    cost = total_cost / iterations
    return cost
