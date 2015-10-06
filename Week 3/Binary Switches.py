###################

lst = [0, 1, 2, 3, 4]


################################

solution2 = []
for i in range(32):
    switches = "{0:05b}".format(i)
    element = []
    for idx in range(len(switches)):
        if int(switches[idx]):
            element.append(lst[idx])       
    solution2.append(element)

for y in solution2:
    print(y)
