# Find the sum of all the multiples of 3 or 5 below 1000.

import numpy as np

u_lim = 1000

arr = np.arange(3, u_lim)
arr = arr[((arr % 3 == 0) | (arr % 5 == 0))]

print(arr.sum())