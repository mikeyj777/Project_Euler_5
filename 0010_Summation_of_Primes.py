# Find the sum of all the primes below two million.

import helpers

primes = helpers.primes_up_to_n_from_full_array(2e6, use_prime_array_for_large_numbers=False)

tot = sum(primes)

print(tot)

