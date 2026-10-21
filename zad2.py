namelist = ["Tom", "Martin","Peter" ]
print (namelist)


#zadanie b
import random
nlist = []
for i in range(5):
    nlist.append(random.randint(1, 100))

print(nlist)

double = [i*2 for i in nlist]
print(double)

for i in range(len(nlist)):
    nlist[i] *= 2

print(nlist)

#zadanie c
def even(lista):
    for x in lista:
        if x % 2 == 0:
            print(x)

def every2(lista):
    for i in range(0, len(lista), 2):
        print(lista[i])

numbers = list(range(1, 11))

print("Liczby parzyste:")
even(numbers)

print("co drugi element:")
every2(numbers)
