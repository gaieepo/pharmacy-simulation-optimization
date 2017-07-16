import simpy
import random
import itertools

NUM_PHAR = 3
SIM_TIME = 3600


class Phar(simpy.Resource):
    def is_done(self):
        return len(self.queue) == 0 and len(self.users) == 0


def patient(name, env, test_event, reg_phar, pac_phar, che_phar, dis_phar, pay_phar):
    print('%s arrived at %.1f' % (name, env.now))
    with reg_phar.request() as req:
        yield req
        print('%s started reg at %.1f' % (name, env.now))
        yield env.timeout(random.lognormvariate(4.5, 1.3))
        print('%s finished reg at %.1f' % (name, env.now))
    with pac_phar.request() as req:
        yield req
        print('%s started pac at %.1f' % (name, env.now))
        yield env.timeout(random.lognormvariate(5.5, 1.4))
        print('%s finished pac at %.1f' % (name, env.now))
    with che_phar.request() as req:
        yield req
        print('%s started che at %.1f' % (name, env.now))
        yield env.timeout(random.lognormvariate(4.8, 1.6))
        print('%s finished che at %.1f' % (name, env.now))
    with dis_phar.request() as req:
        yield req
        print('%s started dis at %.1f' % (name, env.now))
        yield env.timeout(random.lognormvariate(5.0, 1.6))
        print('%s finished dis at %.1f' % (name, env.now))
    with pay_phar.request() as req:
        yield req
        print('%s started pay at %.1f' % (name, env.now))
        yield env.timeout(random.lognormvariate(4.1, 1.2))
        print('%s finished pay at %.1f' % (name, env.now))
    if env.now > SIM_TIME and is_all_done(reg_phar, pac_phar, che_phar, dis_phar, pay_phar):
        test_event.succeed()


def is_all_done(*args):
    for arg in args:
        if not arg.is_done():
            return False
    return True


def patient_generator(env, test_event, reg_phar, pac_phar, che_phar, dis_phar, pay_phar):
    total_time = 0
    for i in itertools.count():
        env.process(patient('Patient %d' % i, env, test_event, reg_phar,
                            pac_phar, che_phar, dis_phar, pay_phar))
        interval = random.expovariate(0.00798)
        total_time += interval
        if total_time > SIM_TIME:
            break
        yield env.timeout(interval)
    yield test_event


random.seed(42)
env = simpy.Environment()

# 2, 3, 1, 4, 1 = 11
reg_phar = Phar(env, capacity=2)
pac_phar = Phar(env, capacity=2)
che_phar = Phar(env, capacity=2)
dis_phar = Phar(env, capacity=3)
pay_phar = Phar(env, capacity=2)


test_event = env.event()
p = env.process(patient_generator(env, test_event, reg_phar,
                                  pac_phar, che_phar, dis_phar, pay_phar))
env.run(until=p)
