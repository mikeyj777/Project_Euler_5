# By considering the terms in the 
# Fibonacci sequence whose values do not exceed four million, find the sum of the even-valued terms.

max_val = 4e6

f0 = 0
f1 = 1
f2 = f0 + f1
ans = 0
tot = 0
while f2 < max_val:
    if f2 % 2 == 0:
        ans += f2
    tot += f2
    print(f'f2: {f2} | even sum {ans} | all sum {tot}')
    f0 = f1
    f1 = f2
    f2 = f0 + f1

print(ans)

# 4613732