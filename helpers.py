import math
import numpy as np
import pandas as pd

def get_primes_up_to_1e9():
    primes_df = pd.read_csv('../proj_euler_data/primes_below_1e9.csv')
    arr = primes_df['prime_number'].to_numpy()
    return arr

def get_starting_matrix_for_prime_testing(num):

    arr = np.arange(5, num + 1, 2)
    arr = arr[arr % 3 != 0]
    arr = arr[((arr % 6 == 1) | (arr % 6 == 5))]

    return arr

def primes_below(num, use_prime_array_for_large_numbers = True, prime_arr = []):
    if num <= 1:
        return
    if num == 2:
        return [2]
    max_prime = int(math.sqrt(num))
    primes = [2, 3]
    if num < 5:
        return primes

    # takes about 9 sec to load primes from csv.  no sense in loading from csv for singular test.
    if len(prime_arr) == 0: 
        if num >= 1e7 and num <= 1e9:
            if use_prime_array_for_large_numbers:
                prime_arr = get_primes_up_to_1e9()

    if len(prime_arr) > 0:
        prime_arr = np.array(prime_arr)
        prime_arr = prime_arr[prime_arr <= num]
        return prime_arr

    arr = get_starting_matrix_for_prime_testing(num)

    while arr[0] < max_prime:
        primes.append(arr[0])
        arr = arr[arr % arr[0] != 0]
    
    primes.extend(arr)
    
    return primes


def is_prime(num, use_prime_array_for_large_numbers = True, prime_arr = []):
    
    if num < 2:
        return False

    if num in [2, 3]:
        return True

    if num % 2 == 0:
        return  False
    
    if num % 3 == 0:
        return False

    if len(prime_arr) == 0:
        if use_prime_array_for_large_numbers:
            if num > 1e7 and num < 1e9:
                prime_arr = get_primes_up_to_1e9()
    
    if len(prime_arr) == 0:
        prime_arr = get_starting_matrix_for_prime_testing(num)

    max_prime_to_check = int(math.sqrt(num))

    i = 0
    while prime_arr[i] <= max_prime_to_check:
        if num % prime_arr[i] == 0:
            return False
        i += 1
    
    return True

def reduce_v_if_check_is_prime(v, check, prime_factors, composite_factors, large_array_of_primes = []):

    check_is_prime = False
    if v % check == 0:
        if check in prime_factors:
            check_is_prime = True
        
        if check not in prime_factors and check not in composite_factors:
            if len(large_array_of_primes) > 0:
                if check in large_array_of_primes:
                    check_is_prime = True
                else:
                    composite_factors[check] = None
            else:
                if is_prime(check):
                    check_is_prime = True
                else:
                    composite_factors[check] = None
    
    if check_is_prime:
        if check not in prime_factors:
            prime_factors[check] = 0
        while v % check == 0:
            prime_factors[check] += 1
            v /= check

    return {
        'v': v,
        'prime_factors': prime_factors,
        'composite_factors': composite_factors,
    }

def get_prime_factors_as_dict_with_values_as_count_of_each_factor(v, prime_factors = {}, composite_factors = {}, large_array_of_primes = []):

    k = 1

    low_primes = [2, 3]
    for p in low_primes:
        resp_dict = reduce_v_if_check_is_prime(v, p, prime_factors, composite_factors)
        v = resp_dict['v']
        prime_factors = resp_dict['prime_factors']
        composite_factors = resp_dict['composite_factors']
        
    upper_check = 6 * k + 1
    lower_check = 6 * k - 1
    while lower_check <= v:
        if k > 10000 and len(large_array_of_primes) == 0:
            large_array_of_primes = get_primes_up_to_1e9()
        resp_dict = reduce_v_if_check_is_prime(v, lower_check, prime_factors, composite_factors, large_array_of_primes)
        v_new = resp_dict['v']
        prime_factors = resp_dict['prime_factors']
        composite_factors = resp_dict['composite_factors']
        if upper_check > v_new:
            break
        
        # probably don't ever have to check upper if lower was a divisor.  however, leaving both in for now.
        # can optimize later if needed.
        resp_dict = reduce_v_if_check_is_prime(v_new, upper_check, prime_factors, composite_factors, large_array_of_primes)
        v_new = resp_dict['v']
        prime_factors = resp_dict['prime_factors']
        composite_factors = resp_dict['composite_factors']
        
        if v_new < v:
            v = v_new
            prime_factors = get_prime_factors_as_dict_with_values_as_count_of_each_factor(v, prime_factors, composite_factors, large_array_of_primes)

        k += 1
        upper_check = 6 * k + 1
        lower_check = 6 * k - 1
    
    return prime_factors
