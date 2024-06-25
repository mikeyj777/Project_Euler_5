# find abc such that a^2 + b^2 = c^2 and a + b + c = 1000.  a, b, c are all natural numbers.

for b in range(1, 1000):
    c = (b**2-1000*b+5e5)/(1000-b)
    if c % 1 != 0:
        continue
    a = 1000 - b - c
    if a % 1 != 0:
        continue
    if a <= 0:
        continue
    if a**2 + b**2 == c**2:
        print(f'a: {a} | b {b} | c {c} | abc {a*b*c}')