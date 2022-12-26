a=int(input("Enter number of numbers in the list:"))
l=[]
for r in range(a):
    b=(input("Enter a value"))
    l.append(b)
b=[]
for r in l:
    if r not in b:
        b.append(r)
print(b, "is the list without duplicates")
