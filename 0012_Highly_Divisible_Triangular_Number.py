# What is the value of the first triangle number to have over five hundred divisors?

import helpers

prime_factors = {}
divisors = {}

max_divisors = -1

for i in range(1, 8):
    tri = i * (i + 1) / 2
    prime_factors[tri] = helpers.get_prime_factors_as_dict_with_values_as_count_of_each_factor(tri)
    
    divisors[tri] = set()
    val = 1
    count = len(prime_factors[tri])
    calc_arr = []
    for prime, max_exp in prime_factors[tri].items():
        calc_arr.append([prime, max_exp])

for i in range(stop = len(calc_arr), step = 2):
    for j in range(calc_arr[i]+1):
        
    apple = 1

apple = 1