import copy

zeroMat = [[0,0],[0,0]]

zeros = zeroMat.copy()

zeros2 = copy.deepcopy(zeroMat)

zeros2[1][1] = 1

print(zeroMat)
