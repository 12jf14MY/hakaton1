with open('task_2.txt') as f:
    s = f.readlines()
print(s)
b = []
n = []
for i in s:
    i = i.replace('\n', '')
    if i.isalpha():
        b.append(i)
    elif i.isdigit():
        n.append(int(i))
print(b, n)
n.sort()
b.sort(key=len)
mas = n + b
print(mas)