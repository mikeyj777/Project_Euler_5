import math
import helpers
import pandas as pd
import numpy as np

from datetime import timedelta
from datetime import datetime as dt

t0 = dt.now()
def prime_timing_test():
    test_vals = np.linspace(6,10,10)

    prime_arr = []

    for val in test_vals:
        t1 = dt.now()
        val_to_test = 10 ** val
        use_stored_primes = False
        if val_to_test >= 1e7:
            use_stored_primes = True
            if len(prime_arr) == 0:
                prime_arr = helpers.get_primes_up_to_1e9()
        arr = helpers.primes_below(val_to_test, use_prime_array_for_large_numbers=use_stored_primes, prime_arr=prime_arr)
        val_is_prime = helpers.is_prime(int(val_to_test))
        dt_1 = dt.now() - t1
        dt_1_0 = dt.now() - t0
        print(f'mag {val} | val {val_to_test} | iter runtime {dt_1} | tot runtime {dt_1_0} | num primes {len(arr)} | val is prime {val_is_prime}')

def prime_size_test(num, use_stored_array = False):
    primes = helpers.primes_below(num, use_prime_array_for_large_numbers=use_stored_array)
    t1 = dt.now()
    dt1 = t1 - t0
    print(f'primes below {num} count: {len(primes)}.  duration: {dt1}')
    prime_test_result = helpers.is_prime(num)
    dt2 = dt.now() - t1
    print(f'test {num} is prime: {prime_test_result}. duration: {dt2}')

# prime_size_test(74207281, use_stored_array=True)

def test_prime_factorization_for_growing_numbers():
    t0 = dt.now()
    primes = helpers.get_primes_up_to_1e9()
    for i in range(1, 101):
        t1 = dt.now()
        val_to_test = np.prod(primes[:i])
        t2 = dt.now()
        dt2_1 = t2 - t1
        p_facts = helpers.get_prime_factors_as_dict_with_values_as_count_of_each_factor(val_to_test)
        t3 = dt.now()
        dt_3_2 = t3 - t2
        dt_3_0 = t3 - t0
        print(f'value: {val_to_test} | prime_dict: {p_facts} | time to get value: {dt2_1} | time to get primes: {dt_3_2} | total runtime {dt_3_0}')
        

def test_prime_factorization_for_random_numbers():
    vals_to_test = np.random.randint(1e8, 1e9, 100, dtype=np.int64)
    t0 = dt.now()
    for val in vals_to_test:
        t1 = dt.now()
        p_facts = helpers.get_prime_factors_as_dict_with_values_as_count_of_each_factor(val)
        t2 = dt.now()
        dt_2_1 = t2 - t1
        dt_2_0 = t2 - t0
        print(f'value: {val} | prime_dict: {p_facts} | time to get primes: {dt_2_1} | total runtime {dt_2_0}')

def test_prime_factorization_for_values_along_6k_pm_1():
    prime_factors = {2: [2], 3: [3]}
    ans = []
    t0 = dt.now()
    t0_1 = t0
    max_k = 100000
    checkstep_mod = int(max_k / 1000)
    for k in range(1,max_k + 1):
        l = 6*k-1
        u = 6*k+1
        
        prime_factors[l] = helpers.get_prime_factors_as_dict_with_values_as_count_of_each_factor(l)
        ans.append([l, len(prime_factors[l])])
        # print(f'{l}: {prime_factors[l]}')
        
        prime_factors[u] = helpers.get_prime_factors_as_dict_with_values_as_count_of_each_factor(u)
        ans.append([u, len(prime_factors[u])])
        # print(f'{u}: {prime_factors[u]}')

        if k % checkstep_mod == 0:
            t1 = dt.now()
            dt1 = t1 - t0_1
            dt1_sec = dt1.total_seconds()
            dt1_0 = t1 - t0
            dt1_0_sec = dt1_0.total_seconds()
            rate = k / dt1_sec
            time_remaining = (max_k - k) / rate
            time_remaining_td = timedelta(seconds=time_remaining)
            est_time_to_complete = dt.now() + time_remaining_td
            print(f'{k} done | last seg dur {int(dt1_sec)} sec | {max_k - k} nums remaining | time left {int(time_remaining)} sec | tot dur {int(dt1_0_sec)} sec | etc {est_time_to_complete.strftime("%Y-%m-%d %H:%M:%S")}')
            t0_1 = t1

    
    ans_df = pd.DataFrame(ans, columns = ['val', 'num_prime_factors'])

    apple = 1

def test_primes_up_to_n(num):
    t_2_0 = dt.now()
    t_2_1 = dt.now()
    report_every_x_primes = 10
    next_reporting_spot = report_every_x_primes
    primes_below = num*math.log(num)
    
    x_0 = primes_below + 1
    X = [x_0]
    p_0 = helpers.get_nth_prime(x_0)
    Y = [p_0]
    if p_0 == num:
        dt_2_2 = dt.now() - t_2_1
        dt_2_2 = dt_2_2.total_seconds()
        print(f'primes up to method took {dt_2_2} seconds')
        return
    x_1 = primes_below + 2
    X.append(x_1)
    p_1 = helpers.get_nth_prime(x_1)
    Y.append(p_1)
    dt_primes = 1
    del_p_output = p_1 - p_0
    x_2 = (x_0 * p_1 - x_1 * p_0) / del_p_output
    X.append(x_2)
    x_0 = x_1
    x_1 = x_2
    p = helpers.get_nth_prime(x_1)
    Y.append(p)

    n = 0
    max_iter = 30
    while p != num and n < max_iter:
        n += 1
        t_2_1 = dt.now()
        p = helpers.get_nth_prime(x_2)
        Y.append(p)
        dt_2_2 = dt.now() - t_2_1
        dt_2_2 = dt_2_2.total_seconds()
        t_2_1 = dt.now()
        dt_2_0 = t_2_1 - t0
        dt_2_0 = dt_2_0.total_seconds()
        if n >= next_reporting_spot:
            print(f'{n} iters so far.  largest prime {p}.  run time {dt_2_0}')
            next_reporting_spot += report_every_x_primes
        del_p_output = p_1 - p_0
        if del_p_output == 0:
            break
        x_2 = (x_0 * p_1 - x_1 * p_0) / del_p_output
        X.append(x_2)
        x_0 = x_1
        x_1 = x_2
    
    
    if p != num:
        n = 0
        while n < max_iter and p != num:
            if len(Y) > len(X):
                Y = Y[:len(X)]
            fit = np.polyfit(Y, X, len(Y)-1)
            x = np.polyval(fit, num)
            X.append(x)
            p = helpers.get_nth_prime(x)
            Y.append(p)
            n += 1
            
    test_time_2 = t_2_1 - t_2_0
    test_time_2 = test_time_2.total_seconds()

    out_str = 'found prime.  '
    if p != num:
        out_str = 'could not get apprpriate prime.  '
        
    print(f'{out_str} run time: {test_time_2}')




def compare_nth_prime_method_to_test_in_is_prime():
    num = 1000000007

    t0 = dt.now()

    test_1 = helpers.is_prime(num)

    t1 = dt.now()

    test_time_1 = t1 - t0
    test_time_1 = test_time_1.total_seconds()

    print(f'is_prime method completed in {test_time_1} sec')

    test_primes_up_to_n(num)

    

compare_nth_prime_method_to_test_in_is_prime()

# print(helpers.get_nth_prime(100))
# print(helpers.is_prime(999983))
# print(helpers.is_prime(289224097))
# test_prime_factorization_for_values_along_6k_pm_1()
# print(helpers.recursive_prime_factoring_to_dict(289224097))

# print(helpers.recursive_prime_factoring_to_dict(978403))
# print(helpers.get_prime_factors_as_dict_with_values_as_count_of_each_factor(289224097))
# stream_crossers = [439357, 992038, 872522]

# test_prime_factorization_for_random_numbers()

# p_facts = helpers.get_prime_factors_as_dict_with_values_as_count_of_each_factor(2*2*3*3*3*23*101*74207281)
# print(p_facts)

# print(helpers.get_prime_factors_as_dict_with_values_as_count_of_each_factor(600851475143))