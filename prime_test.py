import helpers
import pandas as pd
import numpy as np

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

prime_size_test(74207281, use_stored_array=True)