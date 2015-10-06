global counter

def permutations(array):
    global counter
    counter += 1
    if len(array) <= 1:
        return [array]
    res = []
    for permutation in permutations(array[1:]):
        for i in range(len(array)):
            res.append(permutation[:i] + array[0:1] + permutation[i:])
    return res


## TEST

for i in range(5):
    global counter
    counter = 0
    L = [x for x in range(i)]

    all_permutations = permutations(L)

    print()
    print(i, len(all_permutations))


#L = [0, 1, 2, 3, 4, 5]
#L = []
#counter = 0


"""
for item in all_permutations:
    print(item)
"""




