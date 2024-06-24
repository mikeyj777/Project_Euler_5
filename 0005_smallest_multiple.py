# 2520 is the smallest number that can be divided by each of the numbers 
# from 1 to 10 without any remainder.
# What is the smallest positive number that is evenly divisible by all of the numbers
# from 1 to 20?

import numpy as np
import helpers

# the smallest number that is evenly divisible by all numbers from 1 to 20 
# will have the prime factors of every other number.  they don't need to be duplicated 
# bc the answer is only divided by one number bet 1 and 20 at a time. 

all_the_factors = {}
for i in range(2,21):
    prime_factors = helpers.get_prime_factors_as_dict_with_values_as_count_of_each_factor(i)
    for k, v in prime_factors.items():
        if k not in all_the_factors:
            all_the_factors[k] = 0
        all_the_factors[k] = max(all_the_factors[k], v)

ans = 1
for k, v in all_the_factors.items():
    ans *= k**v

print(ans)

# 232792560