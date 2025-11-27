
lista = [1,2,3,4,5]

for i in range(len(lista)):
    i = (i+1)%len(lista)

    print(i)