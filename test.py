import simpy
import random
import itertools

NUM_PHAR = 3
SIM_TIME = 3600 * 9

# SERVE_TIME = random.lognormvariate(4.8, 1.6) + random.lognormvariate(5.0, 1.6)
# random.lognormvariate(4.8, 1.6) + random.lognormvariate(5.0, 1.6)

# phar = Phar(env, NUM_PHAR)

# class Phar:
#     def __init__(self, env, num_phar):
#         self.env = env
#         self.phar_list = simpy.Resource(env, num_phar)

#     def serve(self, patient):
#         yield self.env.timeout(SERVE_TIME)


def patient(name, env, reg_phar, pac_phar, che_phar, dis_phar, pay_phar):
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


def patient_generator(env, reg_phar, pac_phar, che_phar, dis_phar, pay_phar):
    for i in itertools.count():
        env.process(patient('Patient %d' % i, env, reg_phar,
                            pac_phar, che_phar, dis_phar, pay_phar))
        yield env.timeout(random.expovariate(0.00798))


random.seed(42)
env = simpy.Environment()

# 2, 3, 1, 4, 1 = 11
reg_phar = simpy.Resource(env, capacity=2)
pac_phar = simpy.Resource(env, capacity=2)
che_phar = simpy.Resource(env, capacity=2)
dis_phar = simpy.Resource(env, capacity=3)
pay_phar = simpy.Resource(env, capacity=2)


env.process(patient_generator(env, reg_phar,
                              pac_phar, che_phar, dis_phar, pay_phar))
env.run(until=SIM_TIME)
