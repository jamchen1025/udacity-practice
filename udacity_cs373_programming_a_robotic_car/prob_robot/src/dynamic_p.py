grid = [[0, 1, 0, 0, 0, 0],
           [0, 1, 0, 0, 0, 0],
           [0, 1, 0, 0, 0, 0],
           [0, 1, 0, 0, 0, 0],
           [0, 0, 0, 0, 1, 0]]
goal = [len(grid) - 1, len(grid[0]) - 1]
cost = 1
delta = [[-1, 0 ],  # go up
             [ 0, -1],  # go left
             [ 1, 0 ],  # go down
             [ 0, 1 ]]  # go right
delta_name = ['^', '<', 'v', '>']
def compute_value(grid, goal, cost):
    value = [[99 for i in range(len(grid[0]))] for j in range(len(grid))]
    policy = [[' ' for i in range(len(grid[0]))] for j in range(len(grid))]
    change = True
    while change:
        change = False
        for x in range(len(grid)):
            for y in range(len(grid[0])):
                if goal[0] == x and goal[1] == y:
                    if value[x][y] > 0:
                        value[x][y] = 0
                        policy[x][y] = '*'
                        change = True
                elif grid[x][y] == 0:
                    for a in range(len(delta)):
                        x2 = x + delta[a][0]
                        y2 = y + delta[a][1]
                        if x2 >= 0 and x2 < len(grid) and y2 >= 0 and y2 < len(grid[0]):
                            if grid[x2][y2] == 0:
                                v2 = value[x2][y2] + cost
                                if v2 < value[x][y]:
                                    value[x][y] = v2
                                    policy[x][y] = delta_name[a]
                                    change = True
    return policy
p = compute_value(grid, goal, cost)
for i in range(len(p)):
    print(p[i])




