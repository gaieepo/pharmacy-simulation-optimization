import simpy
import random
import itertools

NUM_PHAR = 3
SIM_TIME = 3600 * 9


class Phar(simpy.Resource):
    def is_done(self):
        return len(self.queue) == 0 and len(self.users) == 0


def patient(name, env, data, test_event, reg_phar, pac_phar, che_phar, dis_phar, pay_phar):
    data.setdefault(name, [])
    print('%s arrives at %.1f' % (name, env.now))
    with reg_phar.request() as reg_req:
        data[name].append(env.now)
        print('%s queues reg at %.1f' % (name, env.now))
        yield reg_req
        print('%s starts reg at %.1f' % (name, env.now))
        data[name].append(env.now)
        yield env.timeout(random.uniform(30, 300))
        print('%s finishes reg at %.1f' % (name, env.now))
    with pac_phar.request() as pac_req:
        data[name].append(env.now)
        print('%s queues pac at %.1f' % (name, env.now))
        yield pac_req
        print('%s starts pac at %.1f' % (name, env.now))
        data[name].append(env.now)
        yield env.timeout(random.uniform(120, 480))
        print('%s finishes pac at %.1f' % (name, env.now))
    with che_phar.request() as che_req:
        data[name].append(env.now)
        print('%s queues che at %.1f' % (name, env.now))
        yield che_req
        print('%s starts che at %.1f' % (name, env.now))
        data[name].append(env.now)
        yield env.timeout(random.uniform(10, 300))
        print('%s finishes che at %.1f' % (name, env.now))
    with dis_phar.request() as dis_req:
        data[name].append(env.now)
        print('%s queues dis at %.1f' % (name, env.now))
        yield dis_req
        print('%s starts dis at %.1f' % (name, env.now))
        data[name].append(env.now)
        yield env.timeout(random.uniform(60, 600))
        print('%s finishes dis at %.1f' % (name, env.now))
    with pay_phar.request() as pay_req:
        data[name].append(env.now)
        print('%s queues pay at %.1f' % (name, env.now))
        yield pay_req
        print('%s starts pay at %.1f' % (name, env.now))
        data[name].append(env.now)
        yield env.timeout(random.uniform(30, 180))
        print('%s finishes pay at %.1f' % (name, env.now))
    data[name].append(env.now)
    print('%s leaves at %.1f' % (name, env.now))
    if env.now > SIM_TIME and is_all_done(reg_phar, pac_phar, che_phar, dis_phar, pay_phar):
        test_event.succeed()


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


def patient_generator(env, data, test_event, reg_phar, pac_phar, che_phar, dis_phar, pay_phar):
    total_time = 0
    for i in itertools.count():
        env.process(patient('Patient %d' % i, env, data, test_event, reg_phar,
                            pac_phar, che_phar, dis_phar, pay_phar))
        interval = random.expovariate(0.01190) + 60
        total_time += interval
        if total_time > SIM_TIME:
            break
        yield env.timeout(interval)
    yield test_event


random.seed(42)
env = simpy.Environment()

# 2, 3, 1, 4, 1 = 11
reg_phar = Phar(env, capacity=10)
pac_phar = Phar(env, capacity=10)
che_phar = Phar(env, capacity=10)
dis_phar = Phar(env, capacity=10)
pay_phar = Phar(env, capacity=10)

data = {}
test_event = env.event()
p = env.process(patient_generator(env, data, test_event, reg_phar,
                                  pac_phar, che_phar, dis_phar, pay_phar))
env.run(until=p)
