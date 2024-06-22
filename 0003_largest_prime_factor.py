# What is the largest prime factor of the number 600851475143?

import math
import helpers
import numpy as np

prime_factors_dict = {}

def prime_factors(num):

    global prime_factors_dict

    if num in prime_factors_dict:
        if len(prime_factors_dict[num]) > 0:
            if prime_factors_dict[num] == [num]:
                return

    if num not in prime_factors_dict:
        prime_factors_dict[num] = []

    if num < 2:
        return
    
    if num % 2 == 0:
        prime_factors_dict[num].append(2)
    
    if num % 3 == 0:
        prime_factors_dict[num].append(3)
    
    max_test = int(math.sqrt(num))

    k = 1
    upper_check = 6 * k + 1
    lower_check = 6 * k - 1
    while lower_check <= max_test:
        
        if lower_check in prime_factors_dict:
            if prime_factors_dict[lower_check] == [lower_check]:
                if max_test % lower_check == 0:
                    prime_factors_dict[num].append(lower_check)
        else:
            prime_factors(lower_check)

        if upper_check > max_test:
            break

        if upper_check in prime_factors_dict:
            if prime_factors_dict[upper_check] == [upper_check]:
                if max_test % upper_check == 0:
                    prime_factors_dict[num].append(upper_check)
        else:
            prime_factors(upper_check)
                
        k += 1
        upper_check = 6 * k + 1
        lower_check = 6 * k - 1
    
    prime_factors_dict[num].append(num)

val = 600851475143

prime_factors(val)
