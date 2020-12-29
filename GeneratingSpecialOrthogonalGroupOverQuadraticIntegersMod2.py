# Connor Mooney

from itertools import permutations

residues = [(0,0), (1,0), (0,1), (1,1)]

# This section converts a vector of tuples into a vector that is easy to read
def display(V):
    s = "["
    for i in range(5):
        if V[i] == (0,0):
            s = s + "0   , "
        elif V[i][0] == 0:
            if V[i][1] == 1:
                s = s + "√2  , "
            else:
                s = s + "{}√2  , ".format(V[i][1])
        elif V[i][1] == 0:
            s = s + "{}   , ".format(V[i][0])
        else:
            if V[i][1] == 1:
                s = s + "{}+√2, ".format(V[i][0])
            else:
                s = s + "{}+{}√2, ".format(V[i][0],V[i][1])
    if V[5] == (0,0):
        s = s + "   0]"
    elif V[5][0] == 0:
        if V[5][1] == 1:
            s = s + "  √2]"
        else:
            s = s + "  {}√2]".format(V[5][1])
    elif V[5][1] == 0:
        s = s + "   {}]".format(V[5][0])
    else:
        if V[5][1] == 1:
            s = s + "{}+√2]".format(V[5][0])
        else:
            s = s + "{}+{}√2]".format(V[5][0],V[5][1])
    return s

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
    print(display(v))

possible_pairs = [[],[],[],[],[]]
uniqueness_check = [[],[],[],[]]


# Gives possible pairs and triplets of vectors

for i in range(len(normalized_vects)):
    for j in range(i, len(normalized_vects)):
        uniqueness_check[0]= []
        perms = set(s for s in list(permutations(normalized_vects[j])))
        for perm in perms:
            # Checking for orthogonality
            if dot(normalized_vects[i],perm)[0]%2 == 0 and dot(normalized_vects[i],perm)[1]%2 == 0:
                # Checking for uniqueness of permutation (This should be strong enough now.)
                if perm_check(normalized_vects[i],perm) not in uniqueness_check[0]:
                    uniqueness_check[0].append(perm_check(normalized_vects[i],perm))
                    possible_pairs[0].append([normalized_vects[i],list(perm)])
                    # Does same for triplets etc.
                    for k in range(j, len(normalized_vects)):
                        perms2 = set(s for s in list(permutations(normalized_vects[k])))
                        uniqueness_check[1]=[]
                        for p in perms2:
                            if dot(normalized_vects[i],p)[0]%2 == 0 and dot(normalized_vects[i],p)[1]%2 == 0 and dot(perm,p)[0]%2 == 0 and dot(perm,p)[1]%2 == 0:
                                if perm_check(normalized_vects[i], perm_check(p, perm)) not in uniqueness_check[1]:
                                    uniqueness_check[1].append(perm_check(normalized_vects[i], perm_check(p, perm)))
                                    possible_pairs[1].append([normalized_vects[i],list(perm), list(p)])
                                    for l in range(k, len(normalized_vects)):
                                        perms3 = set(s for s in list(permutations(normalized_vects[l])))
                                        uniqueness_check[2]=[]
                                        for p1 in perms3:
                                            if dot(normalized_vects[i],p1)[0]%2 == 0 and dot(normalized_vects[i],p1)[1]%2 == 0 and dot(perm,p1)[0]%2 == 0 and dot(perm,p1)[1]%2 == 0 \
                                               and dot(p,p1)[0]%2 == 0 and dot(p,p1)[1]%2 == 0:
                                                if perm_check(normalized_vects[i], perm_check(perm_check(p,p1), perm)) not in uniqueness_check[2]:
                                                    uniqueness_check[2].append(perm_check(normalized_vects[i], perm_check(perm_check(p,p1), perm)))
                                                    possible_pairs[2].append([normalized_vects[i],list(perm), list(p), list(p1)])
                                                    for m in range(l, len(normalized_vects)):
                                                        perms4 = set(s for s in list(permutations(normalized_vects[m])))
                                                        uniqueness_check[3]=[]
                                                        for p2 in perms4:
                                                            if dot(normalized_vects[i],p2)[0]%2 == 0 and dot(normalized_vects[i],p2)[1]%2 == 0 and dot(perm,p2)[0]%2 == 0 and dot(perm,p2)[1]%2 == 0 \
                                                               and dot(p,p2)[0]%2 == 0 and dot(p,p2)[1]%2 == 0 and dot(p1,p2)[0]%2==0 and dot(p1,p2)[1]%2==0:
                                                                if perm_check(normalized_vects[i], perm_check(perm, perm_check(p,perm_check(p1,p2)))) not in uniqueness_check[3]:
                                                                    uniqueness_check[3].append(perm_check(normalized_vects[i], perm_check(perm, perm_check(p,perm_check(p1,p2)))))
                                                                    possible_pairs[3].append([normalized_vects[i],list(perm), list(p), list(p1), list(p2)])



print(len(possible_pairs[0]))
print(len(possible_pairs[1]))
print(len(possible_pairs[2]))
print(len(possible_pairs[3]))

txt = open("fiverows.txt","w", encoding="utf-8")

for p in possible_pairs[3]:
    txt.write(display(p[0])+"\n")
    txt.write(display(p[1])+"\n")
    txt.write(display(p[2])+"\n")
    txt.write(display(p[3])+"\n")
    txt.write(display(p[4])+"\n")
    txt.write("\n")
    # This didn't work, so we'll have to think about this more
    #rowsix = []
    #for i in range(len(p[0])):
    #    coli = []
    #    for r in p:
    #        coli.append(r[i])
    #    rowsix.append(((-dot(coli,coli)[0])%4, (-dot(coli,coli)[1])%4))
    #for n in normalized_vects:
    #    permutated = set(s for s in list(permutations(n)))
    #    if rowsix in n:
    #        sixbysix = p.copy().append(rowsix)
    #        possible_pairs[4].append(sixbysix)

print(len(possible_pairs[4]))
txt.close()
#for i in range(len(possible_pairs[0])):
   # print("***************************************************************************")
   # display(possible_pairs[0][i][0])
   # display(possible_pairs[0][i][1])
    
#for p in possible_pairs[1]:
#    print("***************************************************************************")
#    display(p[0])
#    display(p[1])
#   display(p[2])

    
