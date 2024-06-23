# What is the largest prime factor of the number 600851475143?

import math
import helpers
import numpy as np

val = 600851475143

prime_factors = {}
composite_factors = {}

def reduce_v_if_check_is_prime(v, check):
    global prime_factors, composite_factors

    if v % check == 0:
        if check not in prime_factors and check not in composite_factors:
            if helpers.is_prime(check):
                prime_factors[check] = None
                v /= check
            else:
                composite_factors[check] = None
            
    
    return v

def largest_prime_factor(v):

    k = 1

    low_primes = [2, 3]
    for p in low_primes:
        v = reduce_v_if_check_is_prime(v, p)

    upper_check = 6 * k + 1
    lower_check = 6 * k - 1
    while lower_check <= v:
        v = reduce_v_if_check_is_prime(v, lower_check)
        
        if upper_check > v:
            break
        
        # probably don't ever have to check upper if lower was a divisor.  however, leaving both in for now.
        # can optimize later if needed.
        v = reduce_v_if_check_is_prime(v, upper_check)
        
        k += 1
        upper_check = 6 * k + 1
        lower_check = 6 * k - 1


largest_prime_factor(val)

max_factor = max(prime_factors.keys())

print(f'larges prime factor: {max_factor}')

apple = 1

