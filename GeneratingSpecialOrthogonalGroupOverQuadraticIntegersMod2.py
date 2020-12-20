# Connor Mooney

from itertools import permutations

residues = [(0,0), (1,0), (0,1), (1,1)]

# This section converts a vector of tuples into a vector that is easy to read
def display(V):
    s = "["
    for i in range(5):
        if V[i] == (0,0):
            s = s + "0, "
        elif V[i][0] == 0:
            if V[i][1] == 1:
                s = s + "√2, "
            else:
                s = s + "{}√2, ".format(V[i][1])
        elif V[i][1] == 0:
            s = s + "{}, ".format(V[i][0])
        else:
            if V[i][1] == 1:
                s = s + "{}+√2, ".format(V[i][0])
            else:
                s = s + "{}+{}√2, ".format(V[i][0],V[i][1])
    if V[5] == (0,0):
        s = s + "0]"
    elif V[5][0] == 0:
        if V[5][1] == 1:
            s = s + "√2]"
        else:
            s = s + "{}√2]".format(V[5][1])
    elif V[5][1] == 0:
        s = s + "{}]".format(V[5][0])
    else:
        if V[5][1] == 1:
            s = s + "{}+√2]".format(V[5][0])
        else:
            s = s + "{}+{}√2]".format(V[5][0],V[5][1])
    print(s)

# returns dot product   
def dot(v1,v2):
    Sum = [0,0]
    for i in range(len(v1)):
        Sum[0] = Sum[0] + mult(v1[i], v2[i])[0]
        Sum[1] = Sum[1] + mult(v1[i], v2[i])[1]
    return Sum

# Pairwise multiplication mod 2
def pairwise(v1,v2):
    vOut = []
    for i in range(len(v1)):
        vOut.append(mult(v1[i],v2[i]))
    return sorted(vOut)

def perm_check(v1,v2):
    vOut = []
    for i in range(len(v1)):
        vOut.append((*v1[i],*v2[i]))
    return sorted(vOut)

# multiplication of the actual tuples
def mult(n,m):
    if n == (0,0):
       return (0,0)
    elif n == (1,0):
        if m == (0,0):
            return (0,0)
        elif m == (1,0):
            return (1,0)
        elif m == (0,1):
            return (0,1)
        elif m == (1,1):
            return (1,1)
    elif n == (0,1):
        if m == (0,0):
            return (0,0)
        elif m == (1,0):
            return (0,1)
        elif m == (0,1):
            return (2,0)
        elif m == (1,1):
            return (2,1)
    elif n == (1,1):
        if m == (0,0):
            return (0,0)
        elif m == (1,0):
            return (1,1)
        elif m == (0,1):
            return (2,1)
        elif m == (1,1):
            return (3,2)

# Gives all possible vectors 
normalized_vects = [[(1,1),(1,1),(1,1),(1,1),(0,1),(0,1)],[(1,1),(1,1),(1,1),(1,1),(0,0),(0,0)],\
[(1,1),(1,1),(0,1),(0,1),(0,1),(0,0)], [(1,1),(1,1),(0,1),(0,1),(1,0),(1,0)], [(1,1),(1,1),(0,1),(0,0),(0,0),(0,0)],\
[(1,1),(1,1),(1,0),(1,0),(0,0),(0,0)], [(0,1),(0,1),(0,1),(0,1),(0,1),(0,1)], [(0,1),(0,1),(0,1),(0,1),(0,0),(0,0)],\
[(0,1),(0,1),(0,1),(1,0),(1,0),(0,0)], [(0,1),(0,1),(1,0),(1,0),(1,0),(1,0)], [(0,1),(0,1),(0,0),(0,0),(0,0),(0,0)],\
[(0,1),(1,0),(1,0),(0,0),(0,0),(0,0)],[(1,0),(1,0),(1,0),(1,0),(0,0),(0,0)],[(0,0),(0,0),(0,0),(0,0),(0,0),(0,0)]]        
for v in normalized_vects:
    display(v)

possible_pairs = [[],[],[],[]]
uniqueness_check = [[],[],[],[]]


# Gives possible pairs and triplets of vectors
# Doesn't quite agree with 259 pairs - Gives ~494. Since the pairs work, gonna have to think about the permutation part
for i in range(len(normalized_vects)):
    for j in range(i, len(normalized_vects)):
        uniqueness_check[0]= []
        perms = set(s for s in list(permutations(normalized_vects[j])))
        for perm in perms:
            # Checking for orthogonality
            if dot(normalized_vects[i],perm)[0]%2 == 0 and dot(normalized_vects[i],perm)[1]%2 == 0:
                # Checking for uniqueness of permutation (This should be strong enough now. For some reason isn't)
                # Closer but still not quite
                # Need to make it such that a permutation of the pairwise product cannot be in the uniqueness check list either
                if perm_check(normalized_vects[i],perm) not in uniqueness_check[0]:
                    uniqueness_check[0].append(perm_check(normalized_vects[i],perm))
                    possible_pairs[0].append([normalized_vects[i],list(perm)])
                    # Does same for triplets But not quite functional yet
                    for k in range(j, len(normalized_vects)):
                        perms2 = set(s for s in list(permutations(normalized_vects[k])))
                        uniqueness_check[1]=[]
                        for p in perms2:
                            if dot(normalized_vects[i],p)[0]%2 == 0 and dot(normalized_vects[i],p)[1]%2 == 0 and dot(perm,p)[0]%2 == 0 and dot(perm,p)[1]%2 == 0:
                                if perm_check(normalized_vects[i], perm_check(p, perm)) not in uniqueness_check[1]:
                                    uniqueness_check[1].append(perm_check(normalized_vects[i], perm_check(p, perm)))
                                    possible_pairs[1].append([normalized_vects[i],perm, p])


print(len(possible_pairs[0]))
print(len(possible_pairs[1]))
for i in range(len(possible_pairs[0])):
    print("***************************************************************************")
    display(possible_pairs[0][i][0])
    display(possible_pairs[0][i][1])
    
#for p in possible_pairs[1]:
#    print("***************************************************************************")
#    display(p[0])
#    display(p[1])
#   display(p[2])

    
