# Connor Mooney

from itertools import permutations

residues = [(0,0), (1,0), (0,1), (1,1)]

def vectHash(v):
    return hash(tuple(sorted(v)))

def transpose(mat):
    vOut = []
    for i in range(len(mat[0])):
        vOut.append([mat[j][i] for j in range(len(mat))])
    return vOut

def tupleaddition(v):
    num0 = 0
    num1 = 0
    for t in v:
        num0 = num0 + t[0]
        num1 = num1 + t[1]
    return (num0, num1)

def permequivclass(mat):
    return sorted(transpose(sorted(transpose(mat),key = vectHash)))

# SOMEHOW THIS AGREES FOR THE PAIRS, BUT IS NOT STRICT ENOUGH FOR MORE TUPLES. HUH,WE NEED TO FIX THAT SOMEHOW.
# IT BREAKS FOR 3x3 matrices, so we need to fix  it 

def permgenerator(mat):
    perms = []
    for f in permutations(mat):
        for g in permutations(transpose(f)):
            if transpose(g) not in perms:
                perms.append(transpose(g))
    return sorted(perms)

##def isperm(m, n):
##    listm = []
##    for row in m:
##        for element in row:
##            listm.append(element)
##    setm = set(listm)
##    listn = []
##    for row in n:
##        for element in row:
##            listn.append(element)
##    setn = set(listn)
##    if setm != setn:
##        return False
##    mrowsums = []
##    for row in m:
##        mrowsums.append(tupleaddition(row))
##    nrowsums = []
##    for row in n:
##        nrowsums.append(tupleaddition(row))
##    if set(mrowsums) != set(nrowsums):
##        return False
##    mcolsums = []
##    for col in transpose(m):
##        mcolsums.append(tupleaddition(col))
##    ncolsums = []
##    for col in transpose(n):
##        ncolsums.append(tupleaddition(col))
##    if set(mcolsums) != set(ncolsums):
##        return False
##    specialshapeformm = []
##    for row in m:
##        specialshapeformm.append(set(row))
##    specialshapeformm = sorted(specialshapeformm)
##    specialshapeformn = []
##    for row in n:
##        specialshapeformn.append(set(row))
##    specialshapeformn = sorted(specialshapeformn)
##    if specialshapeformn != specialshapeformm:
##        return False
##    if n not in permgenerator(m):
##        return False
##    else:
##        return True

def isperm(m, n):
    # checking if they have the same rows
    specialshapeformm = []
    for row in m:
        specialshapeformm.append(sorted(row))
    specialshapeformm = sorted(specialshapeformm)
    specialshapeformn = []
    for row in n:
        specialshapeformn.append(sorted(row))
    specialshapeformn = sorted(specialshapeformn)
    if specialshapeformn != specialshapeformm:
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
    if transpose(sorted(transpose(n))) in permsnorepeats:
        return True
    else:
        return False


def colpermcheck(m):
    return sorted(transpose(m))

# This section converts a vector of tuples into a vector that is easy to read
def display(V):
    s = "["
    for i in range(len(V)-1):
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
    if V[-1] == (0,0):
        s = s + "   0]"
    elif V[-1][0] == 0:
        if V[-1][1] == 1:
            s = s + "  √2]"
        else:
            s = s + "  {}√2]".format(V[-1][1])
    elif V[-1][1] == 0:
        s = s + "   {}]".format(V[-1][0])
    else:
        if V[-1][1] == 1:
            s = s + "{}+√2]".format(V[-1][0])
        else:
            s = s + "{}+{}√2]".format(V[-1][0],V[-1][1])
    return s

# returns dot product   
def dot(v1,v2):
    Sum = [0,0]
    for i in range(len(v1)):
        Sum[0] = Sum[0] + mult(v1[i], v2[i])[0]
        Sum[1] = Sum[1] + mult(v1[i], v2[i])[1]
    return Sum

def numrowpairs(m):
    numpairs = 0
    valsofpairs = []
    for i in range(len(m)):
        if m[i] not in valsofpairs:
            valcounter = 0
            valsofpairs.append(m[i])
            for j in range(i, len(m)):
                if m[i] == m[j]:
                    valcounter = valcounter + 1
            numpairs = numpairs + int(valcounter/2)
    return numpairs
    
# Pairwise multiplication mod 2
def pairwise(v1,v2):
    vOut = []
    for i in range(len(v1)):
        vOut.append(mult(v1[i],v2[i]))
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

# THIS METHOD WORKS, BUT IT IS TOO SLOW! Need to fix that somehow
# Gives possible pairs and triplets of vectors

checkindex = [0,0,0,0]

for i in range(len(normalized_vects)):
    print("number of pairs: {}".format(len(possible_pairs[0])))
    for j in range(i, len(normalized_vects)):
        checkindex[0] = len(possible_pairs[0])-1
        #print("number of triples: {}".format(len(possible_pairs[1])))
        uniqueness_check[0]= []
        perms = list(list(p) for p in set(s for s in list(permutations(normalized_vects[j]))))
        for perm in perms:
            # Checking for orthogonality
            if dot(normalized_vects[i],perm)[0]%2 == 0 and dot(normalized_vects[i],perm)[1]%2 == 0:
                permquestion = False
                # Checking if row permutations need to be checked also
                for p in possible_pairs[0][checkindex[0]-1:]:
                    if isperm([normalized_vects[i],perm],p):
                        permquestion = True
                        break
                if not permquestion:
                    possible_pairs[0].append([normalized_vects[i],perm])
                    for k in range(j, len(normalized_vects)):
                        checkindex[1] = len(possible_pairs[1])-1
                        #print("number of quadruples: {}".format(len(possible_pairs[2])))
                        uniqueness_check[1]=[]
                        perms2 = list(list(p) for p in set(s for s in list(permutations(normalized_vects[k]))))
                        for p in perms2:
                            if dot(normalized_vects[i],p)[0]%2 == 0 and dot(normalized_vects[i],p)[1]%2 == 0 and dot(perm,p)[0]%2 == 0 and dot(perm,p)[1]%2 == 0:
                                permquestion = False
                                for pe in possible_pairs[1][checkindex[1]-1:]:
                                    if isperm([normalized_vects[i],perm, p], pe):
                                        permquestion = True
                                        break
                                if not permquestion:
                                    possible_pairs[1].append([normalized_vects[i],perm, p])
                                    for l in range(k, len(normalized_vects)):
                                        checkindex[2] = len(possible_pairs[2])-1
                                        perms3 = list(list(p) for p in set(s for s in list(permutations(normalized_vects[l]))))
                                        uniqueness_check[2]=[]
                                        for p1 in perms3:
                                            if dot(normalized_vects[i],p1)[0]%2 == 0 and dot(normalized_vects[i],p1)[1]%2 == 0 and dot(perm,p1)[0]%2 == 0 and dot(perm,p1)[1]%2 == 0 \
                                               and dot(p,p1)[0]%2 == 0 and dot(p,p1)[1]%2 == 0:
                                                permquestion = False
                                                for per in possible_pairs[2][checkindex[2]-1:]:
                                                    if isperm([normalized_vects[i],perm, p, p1], per):
                                                        permquestion = True
                                                        break
                                                if not permquestion:
                                                    possible_pairs[2].append([normalized_vects[i],perm, p, p1])
                                                    for m in range(l, len(normalized_vects)):
                                                        checkindex[3] = len(possible_pairs[3])-1
                                                        perms4 = list(list(p) for p in set(s for s in list(permutations(normalized_vects[m]))))
                                                        uniqueness_check[3]=[]
                                                        for p2 in perms4:
                                                            if dot(normalized_vects[i],p2)[0]%2 == 0 and dot(normalized_vects[i],p2)[1]%2 == 0 and dot(perm,p2)[0]%2 == 0 and dot(perm,p2)[1]%2 == 0 \
                                                               and dot(p,p2)[0]%2 == 0 and dot(p,p2)[1]%2 == 0 and dot(p1,p2)[0]%2==0 and dot(p1,p2)[1]%2==0:
                                                                for perd in possible_pairs[3][checkindex[3]-1:]:
                                                                    if isperm([normalized_vects[i],perm, p, p1, p2], perd):
                                                                        permquestion = True
                                                                        break
                                                                if not permquestion:
                                                                    possible_pairs[3].append([normalized_vects[i],perm, p, p1, p2])


#NEED TO CHECK IF COLUMNS ARE PERPENDICULAR


##for p in possible_pairs[1]:
##    print(display(p[0]))
##    print(display(p[1]))
##    print(display(p[2]))                              
##    print("\n")

                                    
print(len(possible_pairs[0]))
print(len(possible_pairs[1]))
print(len(possible_pairs[2]))
print(len(possible_pairs[3]))

##txt = open("fiverows.txt","w", encoding="utf-8")
##
##for p in possible_pairs[3]:
##    txt.write(display(p[0])+"\n")
##    txt.write(display(p[1])+"\n")
##    txt.write(display(p[2])+"\n")
##    txt.write(display(p[3])+"\n")
##    txt.write(display(p[4])+"\n")
##    txt.write("\n")

for i in range(len(possible_pairs[3])):
    p = possible_pairs[3][i]
    rowsix = []
    for i in range(len(p[0])):
        coli = []
        for r in p:
            coli.append(r[i])
        #print(display(coli))
        rowsix.append(((-dot(coli,coli)[0])%4, (-dot(coli,coli)[1])%4))
    #for i in range(len(p)):
    #    print(display(p[i]))
    #print("Sixth row: " + display(rowsix))
    correctrowsix=[]
    for i in range(len(rowsix)):
        if rowsix[i] == (0,0):
            correctrowsix.append((0,0))
        elif rowsix[i] == (1,0):
            correctrowsix.append((1,0))
        elif rowsix[i] == (2,0):
            correctrowsix.append((0,1))
        elif rowsix[i] == (3,2):
            correctrowsix.append((1,1))
    if len(correctrowsix)==6:
        # Need to also check if this is normalized and orthogonal to all other rows
        # Actuall looks like it already takes care of that, but will have to think about why
        pcop = p.copy()
        pcop.append(correctrowsix)
        possible_pairs[4].append(pcop)
print("Number of full matrices: {}".format(len(possible_pairs[4])))
txt2 = open("sixrows.txt","w", encoding="utf-8")
txt3 = open("sixrowsnopermrepeats.txt", "w", encoding="utf-8")
##txt4 = open("6rowsnoperms2.txt", "w", encoding="utf-8")
genperms = []
for p in possible_pairs[4]:
    already = False
    txt2.write(display(p[0])+"\n")
    txt2.write(display(p[1])+"\n")
    txt2.write(display(p[2])+"\n")
    txt2.write(display(p[3])+"\n")
    txt2.write(display(p[4])+"\n")
    txt2.write(display(p[5])+"\n")
    txt2.write("\n")
# Checking for permutations, but only row and columns separately. Maybe we want to check for all permutations, that is compositions of the two categories?
# Will think about later
##    if sorted(p) not in rowperms:
##        rowperms.append(sorted(p))
##        if colpermcheck(p) not in colperms:
##            colperms.append(colpermcheck(p))
##            for i in range(len(p)):
##                txt3.write(display(p[i])+"\n")
##            txt3.write("\n")
    for g in genperms:
        if isperm(p, g):
            already = True
    if not already:
        genperms.append(p)
        print(len(genperms))

for p in genperms:
    txt3.write(display(p[0])+"\n")
    txt3.write(display(p[1])+"\n")
    txt3.write(display(p[2])+"\n")
    txt3.write(display(p[3])+"\n")
    txt3.write(display(p[4])+"\n")
    txt3.write(display(p[5])+"\n")
    txt3.write("\n")

nopair = []
onepair = []
twopair = []
threepair = []

for m in genperms:
    if numrowpairs(m)==0:
        nopair.append(m)
    elif numrowpairs(m)==1:
        onepair.append(m)
    elif numrowpairs(m)==2:
        twopair.append(m)
    elif numrowpairs(m)==3:
        threepair.append(m)

print(len(nopair))
print(len(onepair))
print(len(twopair))
print(len(threepair))
print("\n")
print(len(genperms))
txt2.close()
txt3.close()
#txt4.close()
print("Written all matrices to `sixrows.txt'")

nopairstxt = open("nopairsmatrix.txt","w", encoding="utf-8")
onepairstxt = open("onepairmatrix.txt","w", encoding="utf-8")
twopairstxt = open("twopairsmatrix.txt","w", encoding="utf-8")
threepairstxt = open("threepairsmatrix.txt","w", encoding="utf-8")

for m in nopair:
    for i in range(len(m)):
        nopairstxt.write(display(m[i])+"\n")
    nopairstxt.write("\n")
for m in onepair:
    for i in range(len(m)):
        onepairstxt.write(display(m[i])+"\n")
    onepairstxt.write("\n")
for m in twopair:
    for i in range(len(m)):
        twopairstxt.write(display(m[i])+"\n")
    twopairstxt.write("\n")
for m in threepair:
    for i in range(len(m)):
        threepairstxt.write(display(m[i])+"\n")
    threepairstxt.write("\n")

nopairstxt.close()
onepairstxt.close()
twopairstxt.close()
threepairstxt.close()


