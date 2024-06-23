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

    # primes above 3 are all of the form 6k+1 or 6k-1
    if (num - 1) / 6 % 1 != 0 and (num + 1) / 6 % 1 != 0:
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

def reduce_v_if_check_is_prime(v, check, prime_factors, composite_factors, large_array_of_primes = [], found_primes = []):

    if check < 100:
        if check not in found_primes:
            if is_prime(check):
                found_primes.append(check)

    check_is_prime_factor = False
    if v % check == 0:
        if check in prime_factors or check in found_primes:
            check_is_prime_factor = True
        
        if check not in prime_factors and check not in composite_factors and check not in found_primes:
            if len(large_array_of_primes) > 0:
                if check in large_array_of_primes:
                    check_is_prime_factor = True
            else:
                check_has_factor_in_found_primes = False
                for p in found_primes:
                    if check % p == 0:
                        check_has_factor_in_found_primes = True
                        break
                if not check_has_factor_in_found_primes:
                    if is_prime(check, prime_arr=large_array_of_primes):
                        check_is_prime_factor = True
                        found_primes.append(check)
    
        if check_is_prime_factor:
            if check not in prime_factors:
                prime_factors[check] = 0
            while v % check == 0:
                prime_factors[check] += 1
                v /= check
        else:
            if check not in composite_factors:
                composite_factors[check] = 1

    return {
        'v': v,
        'prime_factors': prime_factors,
        'composite_factors': composite_factors,
        'found_primes': found_primes
    }

def get_prime_factors_as_dict_with_values_as_count_of_each_factor(v):

    prime_factors = {}
    composite_factors = {}
    large_array_of_primes = []
    found_primes = []

    low_primes = [2, 3]
    for p in low_primes:
        resp_dict = reduce_v_if_check_is_prime(v, p, prime_factors, composite_factors, found_primes=found_primes)
        v = resp_dict['v']
        prime_factors = resp_dict['prime_factors']
        composite_factors = resp_dict['composite_factors']
        found_primes = resp_dict['found_primes']

    k = 1
    u = 0
    upper_check = 6 * k + 1
    lower_check = 6 * k - 1
    while lower_check <= v:
        if k > 10000 and u == 0:
            u = int(v / 6)
            u_upper = 6 * k + 1
            u_lower = 6 * k - 1
        
        if k > 100000 and len(large_array_of_primes) == 0:
            large_array_of_primes = get_primes_up_to_1e9()
        
        resp_dict = reduce_v_if_check_is_prime(v, lower_check, prime_factors, composite_factors, large_array_of_primes, found_primes=found_primes)
        v = resp_dict['v']
        prime_factors = resp_dict['prime_factors']
        composite_factors = resp_dict['composite_factors']
        if upper_check > v:
            break
        
        # probably don't ever have to check upper if lower was a divisor.  however, leaving both in for now.
        # can optimize later if needed.
        resp_dict = reduce_v_if_check_is_prime(v, upper_check, prime_factors, composite_factors, large_array_of_primes, found_primes=found_primes)
        v = resp_dict['v']
        prime_factors = resp_dict['prime_factors']
        composite_factors = resp_dict['composite_factors']
        
        if u > 0:
            if u < k:
                print('streams crossed')
                prime_factors[v] = 1
                break
            
            resp_dict = reduce_v_if_check_is_prime(v, u_upper, prime_factors, composite_factors, large_array_of_primes)
            v = resp_dict['v']
            prime_factors = resp_dict['prime_factors']
            composite_factors = resp_dict['composite_factors']

            resp_dict = reduce_v_if_check_is_prime(v, u_lower, prime_factors, composite_factors, large_array_of_primes)
            v = resp_dict['v']
            prime_factors = resp_dict['prime_factors']
            composite_factors = resp_dict['composite_factors']
            u -= 1
            u_upper = 6 * k + 1
            u_lower = 6 * k - 1


        k += 1
        upper_check = 6 * k + 1
        lower_check = 6 * k - 1
    
    return prime_factors

def recursive_prime_factoring_to_dict(v, prime_factors_of_each_number = {}, prime_factors = {}, composite_factors = {}, found_primes=[]):
    if len(prime_factors_of_each_number) == 0:
        prime_factors_of_each_number[2] = [2]
        prime_factors_of_each_number[3] = [3]
    
    if v < 5:
        return
    
    l = 1
    l_l = 5 * l - 1
    l_u = 5 * l + 1

    while 

