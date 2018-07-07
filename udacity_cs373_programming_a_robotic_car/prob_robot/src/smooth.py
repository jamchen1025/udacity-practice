import matplotlib.pyplot as plt

path = [[0, 0], [1, 0], [2, 0], [3, 0], [4, 0], [5, 0],
            [6, 0], [6, 1], [6, 2],
            [6, 3], [5, 3], [4, 3], [3, 3], [2, 3], [1, 3],
            [0, 3], [0, 2], [0, 1]]
fix_points = [1, 0, 0, 0, 0, 0,
                    1, 0, 0,
                    1, 0, 0, 0, 0, 0,
                    1, 0, 0]

def smooth(path, weight_data=0.2, weight_smooth=0.1, tolerance=0.000001):
    newpath = [[0 for i in range(len(path[0]))] for j in range(len(path))]
    for i in range(len(path)):
        for j in range(len(path[0])):
            newpath[i][j] = path[i][j]
    change = tolerance
    while change >= tolerance:
        change = 0.0
        len_p = len(path)
        for i in range(len_p):
            for j in range(len(path[0])):
                aux = newpath[i][j]
                newpath[i][j] += weight_data * (path[i][j] - newpath[i][j])
                newpath[i][j] += weight_smooth * (newpath[(i - 1) % len_p][j] 
                                                  + newpath[(i + 1) % len_p][j] 
                                                  - 2.0 * newpath[i][j])
                newpath[i][j] += 0.5 * weight_smooth * (2.0 * newpath[(i - 1) % len_p][j] 
                                                  - newpath[(i - 2) % len_p][j] 
                                                  - newpath[i][j])
                newpath[i][j] += 0.5 * weight_smooth * (2.0 * newpath[(i + 1) % len_p][j] 
                                                  - newpath[(i + 2) % len_p][j] 
                                                  - newpath[i][j])
                change += abs(aux - newpath[i][j])
    return newpath

def getxy(path):
    x = []
    y = []
    for i in range(len(path)):
        x.append(path[i][0])
        y.append(path[i][1])
    return x, y

def printpaths(path, newpath):
    x1, y1 = getxy(path)
    x2, y2 = getxy(newpath)
    
    plt.figure(2)
    plt.plot(x1, y1, 'r', label='path')
    plt.plot(x2, y2, 'g', label='newpath')
    plt.legend()
    plt.show()
    
printpaths(path, smooth(path))
