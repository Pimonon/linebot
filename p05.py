def cube(x):
    return x**3

def power(x,y):
        return x**y

def fac(x):
    if x == 1:
        return 1
    if x ==2:
         return 2
    return x * fac(x-1)

x = 2
y = cube(x)

print(x,y)

print(power (5,2))

#print('FAC' fac(1000))


