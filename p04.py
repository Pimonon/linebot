L = [50,2,5,3,6,7,0,8,77,9]

print(L) # -->2
print(L[1])
print('Last:',L[7])
print('Last:',L[-1])

L2 = L[1:4] #Slice
print(L2)

for x in L:
    print(x)

a = len(L)
print('Length = ',a)

for i in range(a):
    print(i, L[i])

L.sort(reverse=True)
print(L)


# Bubble sort
for i in range(a-1):
    for j in range(a-1):
        if L[j] > L[j+1]:
            L[j],L[j+1] = L[j+1],L[j]
print(L)

print(type(a))
print(type(L))


