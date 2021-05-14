from itertools import permutations

def transpose(mat):
    vOut = []
    for i in range(len(mat[0])):
        vOut.append([mat[j][i] for j in range(len(mat))])
    return vOut


def isperm(m, n):
    # checking if they have the same rows
    specialshapeformm = []
    for row in m:
        specialshapeformm.append(sorted(row))
    specialshapeformm = sorted(specialshapeformm)
    #print(specialshapeformm)
    specialshapeformn = []
    for row in n:
        specialshapeformn.append(sorted(row))
    specialshapeformn = sorted(specialshapeformn)
    #print(specialshapeformn)
    if specialshapeformn != specialshapeformm:
        #print("Not same row classes")
        return False

    # First, we find all the rows permutations of m
    # We then sort all of them and see if the sorted form of n is in

    perms = list(permutations(m))
    permsnorepeats = []
    for p in perms:
        permsnorepeats.append(p)
        if p in permsnorepeats[0:-1]:
            permsnorepeats.pop()
    for i in range(len(permsnorepeats)):
        permsnorepeats[i] = transpose(sorted(transpose(permsnorepeats[i])))
    #print(transpose(sorted(transpose(n))))
    #print(permsnorepeats)
    if transpose(sorted(transpose(n))) in permsnorepeats:
        return True
    else:
        return False

#print(isperm([[1,3,4],[1,3,4], [5,3,2]], [[3,1,4], [3,1,4], [3,5,2]]))


for p in permutations([[1,0,0],[0,1,1],[1,0,1]]):
    for c in permutations(transpose(p)):
        print(isperm(transpose(c), [[1,1,0],[1,1,0],[0,0,1]]))

