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
