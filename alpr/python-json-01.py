import json

print('Hello')
emp1 = {
    'name':'Nuchnat',
    'age':18,
    'cats':['patui','ew']
}
emp2 = {
    'name':'Uthumphon',
    'age':25
}
print(json.dumps(emp1,sort_keys=True,indent=4))
print(emp2['name'], emp2['age'])
employees = []
employees.append(emp1)
employees.append(emp2)
sum = 0
for e in employees:
    sum += e['age']
l = len(employees)
print(sum/l)

for e in employees:
    for k in e:
        print(k,e[k])
    # print('Name:',e['name'])
    # print('Age:',e['age'])
    # print('Cats:',e['cats'])