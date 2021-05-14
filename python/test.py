def colpermcheck(mat):
    vOut = []
    for i in range(len(mat[0])):
        vOut.append([mat[j][i] for j in range(len(mat))])
    return sorted(vOut)

print(colpermcheck(sorted([[(1,1),(0,0),(1,0)], [(0,0),(0,1),(1,1)]])))
