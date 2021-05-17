import numpy as np
import copy

# Generating Pattern Representatives
# The format of the matrices is that each entry is represented by a triple (a,b,c)=(a+b*sqrt(2))/(sqrt(2)^c)
zeroMat = [[(0,0,0),(0,0,0),(0,0,0),(0,0,0),(0,0,0),(0,0,0)],[(0,0,0),(0,0,0),(0,0,0),(0,0,0),(0,0,0),(0,0,0)],[(0,0,0),(0,0,0),(0,0,0),(0,0,0),(0,0,0),(0,0,0)], \
           [(0,0,0),(0,0,0),(0,0,0),(0,0,0),(0,0,0),(0,0,0)],[(0,0,0),(0,0,0),(0,0,0),(0,0,0),(0,0,0),(0,0,0)],[(0,0,0),(0,0,0),(0,0,0),(0,0,0),(0,0,0),(0,0,0)]]

noneMat = [[None, None, None, None, None, None], [None, None, None, None, None, None], \
          [None, None, None, None, None, None], [None, None, None, None, None, None],\
          [None, None, None, None, None, None], [None, None, None, None, None, None]]

def transpose(mat):
    """returns the transpose of a matrix"""
    vOut = []
    for i in range(len(mat[0])):
        vOut.append([mat[j][i] for j in range(len(mat))])
    return vOut


# Need to revamp the permutation to also cover row permutations
def colpermcheck(m):
    """returns the column-permutation invariant normal form of a matrix"""
    return transpose(sorted(transpose(m)))


def CliffCheck(m):
    cliff = True
    for row in m:
        for tup in row:
            if tup[2]%2 != 0:
                cliff = False
    return cliff

def lengthnormalizer(strd, num):
    s = strd
    for i in range(num-len(strd)):
        s = s + " "
    return s

def isperm(mat1, mat2):
    check = matmult(transpose(mat1), mat2)
    i = 0
    j = 0
    cols = [0,1,2,3,4,5]
    while i<6:
        if check[i][cols[j]] not in [(0,0,0),(1,0,0),(-1,0,0)]:
            return False
        elif check[i][cols[j]] == (0,0,0) and (j<len(cols)-1):
            j = j+1
        else:
            i = i+1
            cols.pop(j)
            j = 0
    return True

# WILL IMPROVE LATER
def tupledisplay(tup):
    if tup[2] == 0:
        if tup[0] == 0:
            if tup[1] == 0:
                return lengthnormalizer("0",15)
            elif tup[1] == 1:
                return lengthnormalizer("√2",15)
            else:
                return lengthnormalizer("{}√2".format(tup[1]),15)
        elif tup[0] == 1:
            if tup[1] == 0:
                return lengthnormalizer("1",15)
            elif tup[1] == 1:
                return lengthnormalizer("1+√2",15)
            else:
                return lengthnormalizer("1+{}√2".format(tup[1]),15)
        else:
            if tup[1] == 0:
                return lengthnormalizer("{}".format(tup[0]),15)
            elif tup[1] == 1:
                return lengthnormalizer("{}+√2".format(tup[0]),15)
            else:
                return lengthnormalizer("{}+{}√2".format(tup[0],tup[1]),15)
    elif tup[2] == 1:
        if tup[0] == 0:
            if tup[1] == 0:
                return lengthnormalizer("0",15)
            elif tup[1] == 1:
                return lengthnormalizer("√2/√2",15)
            else:
                return lengthnormalizer("{}√2/√2".format(tup[1]),15)
        elif tup[0] == 1:
            if tup[1] == 0:
                return lengthnormalizer("1/√2",15)
            elif tup[1] == 1:
                return lengthnormalizer("(1+√2)/√2",15)
            else:
                return lengthnormalizer("(1+{}√2)/√2".format(tup[1]),15)
        else:
            if tup[1] == 0:
                return lengthnormalizer("{}/√2".format(tup[0]),15)
            elif tup[1] == 1:
                return lengthnormalizer("({}+√2)/√2".format(tup[0]),15)
            else:
                return lengthnormalizer("({}+{}√2)/√2".format(tup[0],tup[1]),15)

    else:
        if tup[0] == 0:
            if tup[1] == 0:
                return lengthnormalizer("0",15)
            elif tup[1] == 1:
                return lengthnormalizer("√2/(√2^{})".format(tup[2]),15)
            else:
                return lengthnormalizer("{}√2/(√2^{})".format(tup[1],tup[2]),15)
        elif tup[0] == 1:
            if tup[1] == 0:
                return lengthnormalizer("1/(√2^{})".format(tup[2]),15)
            elif tup[1] == 1:
                return lengthnormalizer("(1+√2)/(√2^{})".format(tup[2]),15)
            else:
                return lengthnormalizer("(1+{}√2)/(√2^{})".format(tup[1],tup[2]),15)
        else:
            if tup[1] == 0:
                return lengthnormalizer("{}/(√2^{})".format(tup[0],tup[2]),15)
            elif tup[1] == 1:
                return lengthnormalizer("({}+√2)/(√2^{}) ".format(tup[0],tup[2]),15)
            else:
                return lengthnormalizer("({}+{}√2)/(√2^{})".format(tup[0],tup[1],tup[2]),15)

    

def listdisplay(li):
    listr = "["
    for t in li:
        listr = listr + tupledisplay(t) + ", "
    listr = listr[0:-2] + "]"
    return listr

def matdisplay(M):
    mat = ""
    for row in M:
        mat = mat + listdisplay(row) + "\n"
    return mat

def tupmult(t1, t2):
    if (t1[0] == 0 and t1[1] == 0) or (t2[0] == 0 and t2[1] == 0):
        return (0,0,0)
    t3 = (t1[0]*t2[0]+2*t1[1]*t2[1], t1[1]*t2[0]+t1[0]*t2[1],t1[2]+t2[2])
    while t3[0]%2 == 0 and t3[2] > 0:
        t3 = (t3[1], int(t3[0]/2), t3[2]-1)
    return t3

def tupadd(t1, t2):
    t1cop = (t1[0], t1[1], t1[2])
    t2cop = (t2[0], t2[1], t2[2])
    if t1[2] <= t2[2]:
        while t2cop[2] > t1cop[2]:
            t1cop = (2*t1cop[1], t1cop[0], t1cop[2]+1)
        t3 = (t1cop[0] + t2cop[0], t1cop[1] + t2cop[1], t2cop[2])
    else:
        while t1cop[2] > t2cop[2]:
            t2cop = (2*t2cop[1], t2cop[0], t2cop[2]+1)
        t3 = (t1cop[0] + t2cop[0], t1cop[1] + t2cop[1], t2cop[2])
    if t3[0] == 0 and t3[1] == 0:
        return (0,0,0)
    while t3[0]%2 == 0 and t3[2]>0:
        t3 = (t3[1], int(t3[0]/2), t3[2]-1)
    return t3

def matmult(m1, m2):
    """Multiplies to matrices together"""
    m3 = copy.deepcopy(noneMat)
    for i in range(6):
        for j in range(6):
            m3[i][j] = tupadd(tupmult(m1[i][0],m2[0][j]),tupadd(tupmult(m1[i][1],m2[1][j]),\
                    tupadd(tupmult(m1[i][2],m2[2][j]), tupadd(tupmult(m1[i][3],m2[3][j]),\
                    tupadd(tupmult(m1[i][4],m2[4][j]), tupmult(m1[i][5],m2[5][j]))))))
    return m3

def leastdenompower(m):
    """ Returns the least denominator power of a matrix"""
    maximum = 0
    for row in m:
        for entry in row:
            if entry[2]>=maximum:
                maximum = entry[2]
    return maximum

def residue(m):
    """Returns the residue of a matrix in SO_6(Z[1/sqrt(2))"""
    cop = copy.deepcopy(m)
    leastpower = leastdenompower(m)
    for row in cop:
        for entry in row:
            for i in range(leastpower - entry[2]):
                entry = (2*entry[1], entry[0], entry[2] + 1)
    residues = copy.deepcopy(noneMat)
    for i in range(len(cop)):
        for j in range(len(cop[0])):
            residues[i][j] = (entry[0]%2, entry[1]%2)
    return residues


# NEED TO UPDATE
def Tmat(i, j):
    """Returns T_{ij} after mapped to SO_6(Z[1/sqrt(2))"""
    Ttoreturn = copy.deepcopy(zeroMat)
    Ttoreturn[i-1][j-1] = (-1,0,1)
    Ttoreturn[i-1][i-1], Ttoreturn[j-1][i-1], Ttoreturn[j-1][j-1] = (1,0,1), (1,0,1), (1,0,1)
    for k in range(0,6):
        if k != i-1 and k != j-1:
            Ttoreturn[k][k] = (1,0,0)
    return(Ttoreturn)


def fileoutput(m, tcount, string):
    s = "****************\n\n"
    s = s + "pattern: \n"
    s = s + matdisplay(m)+ "\n"
    s = s + "Tcount: {} \n".format(tcount)
    s = s + "residue: {} \n".format(residue(m))
    s = s + "String: {} \n\n".format(string)
    return s


# RELEVANT LISTS

Ts = [Tmat(1,2), Tmat(1,3), Tmat(1,4), Tmat(1,5), Tmat(1,6), Tmat(2,3), Tmat(2,4), Tmat(2,5), Tmat(2,6), Tmat(3,4), Tmat(3,5), Tmat(3,6), Tmat(4,5), Tmat(4,6), Tmat(5,6)]
Tlabels = ["T12","T13","T14","T15","T16","T23","T24","T25","T26","T34","T35","T36","T45","T46","T56"]
tcountpatterns = [[],[],[],[],[]]
allmats = []


# GENERATING PATTERNS

txt = open("patterns.txt","w", encoding="utf-8")

for i in range(len(Ts)):
    tcountpatterns[0].append((Ts[i], Tlabels[i]))
    allmats.append(Ts[i])
    txt.write(fileoutput(Ts[i], 1, Tlabels[i]))

print(len(tcountpatterns[0]))

# NEED TO REVAMP THIS CODE
for j in range(1,2):
    for i in range(len(Ts)):
        for tup in tcountpatterns[j-1]:
            # Checks if it's not a column permutation
            prod = matmult(tup[0], Ts[i])
            if not CliffCheck(prod):
                perm = False
                for m in allmats:
                    if isperm(m, prod):
                        perm = True
                if not perm:
                    tcountpatterns[j].append((prod, tup[1]+Tlabels[i]))
                    allmats.append(prod)
                    txt.write(tup[1]+Tlabels[i])

    print(len(tcountpatterns[j]))
##            if colpermcheck(matmult(tup[0],Ts[i])) not in allmats:
##                # Checks if it's not a clifford matrix
##                if not CliffCheck(matmult(tup[0],Ts[i])):
##                    tcountpatterns[j].append((matmult(tup[0],Ts[i]), tup[1]+Tlabels[i]))
##                    allmats.append(colpermcheck(matmult(tup[0],Ts[i])))
##                    txt.write(fileoutput(tup[0],j+1, tup[1]+Tlabels[i]))

for row in tcountpatterns:
    print(len(row))
