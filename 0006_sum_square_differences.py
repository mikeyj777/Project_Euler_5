# Find the difference between the sum of the squares of the first one hundred
# natural numbers and the square of the sum

def sum_squares_up_to_n(n):
    return n * (n+1) * (2*n + 1) / 6

def sum_of_n_natural_numbers_total_squared(n):
    val = n*(n+1)/2
    return val**2

n = 100
print(sum_of_n_natural_numbers_total_squared(n) - sum_squares_up_to_n(n))

# 25164150