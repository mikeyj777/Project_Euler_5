# A palindromic number reads the same both ways. 
# Find the largest palindrome made from the product of two 3-digit numbers.

import numpy as np

prods = []
for i in range(999, 99, -1):
    for j in range(999, 99, -1):
        prod = i * j
        prods.append(prod)

prods.sort(reverse=True)

for prod in prods:
    prod_str = str(prod)
    prod_len = len(prod_str)
    foreward = 0
    backward = -1
    is_palindrome = True
    while foreward <= prod_len / 2:
        if prod_str[foreward] != prod_str[backward]:
            is_palindrome = False
            break
        foreward += 1
        backward -= 1
    if is_palindrome:
        print(prod)
        
# 906609