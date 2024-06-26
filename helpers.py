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

    if v is None:
        return {}

    if v <= 1:
        return {1: 1}

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

def recurse_checker(v, check, prime_factors_of_each_number, found_primes = set()):
    v_orig = v
    if check not in prime_factors_of_each_number:
        prime_factors_of_each_number = recursive_prime_factoring_to_dict(check, prime_factors_of_each_number)
        check_is_prime = True
        for k, _ in prime_factors_of_each_number[check].items():
            if k != check:
                check_is_prime = False
        if not check_is_prime:
            return {
                'v': v,
                'prime_factors_of_each_number': prime_factors_of_each_number
            }
        found_primes.add(check)
    if check not in prime_factors_of_each_number[v_orig]:
        if len(prime_factors_of_each_number[check]) == 1:
            if v % check == 0:
                count = 0
                while v % check == 0:
                    v /= check
                    count += 1
                if check not in prime_factors_of_each_number[v_orig]:
                    prime_factors_of_each_number[v_orig][check] = 0
                prime_factors_of_each_number[v_orig][check] += count
            # will run if v is updated
            if v >= 2:
                if v not in prime_factors_of_each_number:
                    prime_factors_of_each_number = recursive_prime_factoring_to_dict(v, prime_factors_of_each_number)
        
    return {
        'v': v,
        'prime_factors_of_each_number': prime_factors_of_each_number,
        'found_primes': found_primes
    }

def recursive_prime_factoring_to_dict(v, prime_factors_of_each_number = {}):

    if v in prime_factors_of_each_number:
        return prime_factors_of_each_number
    
    prime_factors_of_each_number[v] = {}
    if v < 100000:
        if is_prime(v):
            prime_factors_of_each_number[v] = {v: 1} 
            return prime_factors_of_each_number
    
    v_orig = v

    for p in [2, 3]:
        if v == 9:
            apple = 1
        resp_dict = recurse_checker(v = v, check= p, prime_factors_of_each_number=prime_factors_of_each_number)
        v = resp_dict['v']
        prime_factors_of_each_number = resp_dict['prime_factors_of_each_number']
        if v == 1:
            break
        if v < v_orig and v in prime_factors_of_each_number:
            prime_factors_of_each_number[v_orig].update(prime_factors_of_each_number[v].copy())
        
        # prime_factors_of_each_number[v_orig].extend(prime_factors_of_each_number[v])
    
    if v < 2:
        return prime_factors_of_each_number

    l = 1
    l_l = 6 * l - 1
    l_u = 6 * l + 1

    while l_l < v:
        if l_l == 5 or (l_l % 5 != 0 and l_l % 7 != 0):

            resp_dict = recurse_checker(v = v, check= l_l, prime_factors_of_each_number=prime_factors_of_each_number)
            v = resp_dict['v']
            prime_factors_of_each_number = resp_dict['prime_factors_of_each_number']
            # prime_factors_of_each_number[v_orig].extend(prime_factors_of_each_number[v])
            if v < v_orig and v in prime_factors_of_each_number:
                prime_factors_of_each_number[v_orig].update(prime_factors_of_each_number[v].copy())

        if l_u > v:
            break
        
        if l_u == 7 or (l_u % 5 !=0 and l_u % 7 != 0):
            resp_dict = recurse_checker(v = v, check= l_u, prime_factors_of_each_number=prime_factors_of_each_number)
            v = resp_dict['v']
            prime_factors_of_each_number = resp_dict['prime_factors_of_each_number']
            if v < v_orig and v in prime_factors_of_each_number:
                prime_factors_of_each_number[v_orig].update(prime_factors_of_each_number[v].copy())
            # prime_factors_of_each_number[v_orig].extend(prime_factors_of_each_number[v])

        l += 1
        l_l = 6 * l - 1
        l_u = 6 * l + 1

    if len(prime_factors_of_each_number[v_orig]) == 0:
            prime_factors_of_each_number[v_orig] = {v_orig: 1}


    return prime_factors_of_each_number

def test_primes_up_to_n(n, primes_so_far = {}):

    primes_arr = np.array(list(primes_so_far.keys()))
    test_for_existing_prime_factors = n % primes_arr
    if 0 not in test_for_existing_prime_factors:
        primes_so_far[n] = None
        
    return primes_so_far

def get_nth_prime(n):

    primes = {}
    primes[2] = None
    primes[3] = None

    k = 0
    primes_display_step = 1000
    primes_display_cutoff = primes_display_step
    while len(primes) < n:
        k += 1
        l = 6*k - 1
        u = 6*k + 1
        primes = test_primes_up_to_n(l, primes_so_far=primes)
        if len(primes) == n:
            break
        primes = test_primes_up_to_n(u, primes_so_far=primes)
        
        # if len(primes) > primes_display_cutoff:
        #     largest_prime = max(primes.keys())
        #     pi = largest_prime / math.log(largest_prime)
        #     print(f'{len(primes)} found.  {n - len(primes)} to go. largest prime {max(primes.keys())}.  pi accuracy {(pi-len(primes))/len(primes)}')
        #     primes_display_cutoff += primes_display_step

    return max(primes.keys())

def get_primes_up_to_n(n):

    if n < 2:
        return []
    
    if n == 2:
        return [2]
    
    if n < 5:
        return [2, 3]

    primes = {}
    primes[2] = None
    primes[3] = None

    k = 0
    primes_display_step = 1000
    primes_display_cutoff = primes_display_step
    largest_prime = 3
    while largest_prime < n:
        k += 1
        l = 6*k - 1
        u = 6*k + 1
        primes = test_primes_up_to_n(l, primes_so_far=primes)
        largest_prime = max(primes.keys())
        if largest_prime == n:
            break
        primes = test_primes_up_to_n(u, primes_so_far=primes)
        
        largest_prime = max(primes.keys())
        if len(primes) > primes_display_cutoff:
            
            pi = largest_prime / math.log(largest_prime)
            print(f'{len(primes)} found.  {n - len(primes)} to go. largest prime {largest_prime}.  pi accuracy {(pi-len(primes))/len(primes)}')
            primes_display_cutoff += primes_display_step

    return list(primes.keys())

def primes_up_to_n_from_full_array(num, use_prime_array_for_large_numbers = True, prime_arr = []):
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


