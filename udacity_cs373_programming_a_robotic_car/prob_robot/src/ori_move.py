grid = [[1, 1, 1, 0, 0, 0],
           [1, 1, 1, 0, 1, 0],
           [0, 0, 0, 0, 0, 0],
           [1, 1, 1, 0, 1, 1],
           [1, 1, 1, 0, 1, 1]]
init = [4, 3, 0]  # ori = 0: up 1: left  2: down 3: right
goal = [2, 0]
cost = [2, 1, 20] 
forward = [[-1, 0],  # go up
                 [ 0, -1],  # go left
                 [ 1, 0],  # go down
                 [ 0, 1]]  # go right
forward_name = ['up', 'left', 'down', 'right']
action = [-1, 0, 1]
action_name = ['R', '#', 'L']

def optimum_policy2D(grid, init, goal, cost):
    value = [
    [[999 for i in range(len(grid[0]))] for j in range(len(grid))],
    [[999 for i in range(len(grid[0]))] for j in range(len(grid))],
    [[999 for i in range(len(grid[0]))] for j in range(len(grid))],
    [[999 for i in range(len(grid[0]))] for j in range(len(grid))]]
    policy = [
    [[' ' for i in range(len(grid[0]))] for j in range(len(grid))],
    [[' ' for i in range(len(grid[0]))] for j in range(len(grid))],
    [[' ' for i in range(len(grid[0]))] for j in range(len(grid))],
    [[' ' for i in range(len(grid[0]))] for j in range(len(grid))]]
    policy2D = [[' ' for i in range(len(grid[0]))] for j in range(len(grid))]
    change = True
    while change:
        change = False
        for x in range(len(grid)):
            for y in range(len(grid[0])):
                for ori in range(4):
                    if goal[0] == x and goal[1] == y:
                        if value[ori][x][y] > 0:
                            value[ori][x][y] = 0
                            policy[ori][x][y] = '*'
                            change = True
                    elif grid[x][y] == 0:
                        for i in range(3):
                            o2 = (ori + action[i]) % 4
                            x2 = x + forward[o2][0]
                            y2 = y + forward[o2][1]
                            if x2 >= 0 and x2 < len(grid) and y2 >= 0 and y2 < len(grid[0]):
                                if grid[x2][y2] == 0:
                                    v2 = value[o2][x2][y2] + cost[i]
                                    if v2 < value[ori][x][y]:
                                        value[ori][x][y] = v2
                                        policy[ori][x][y] = action_name[i]
                                        change = True
    x = init[0]
    y = init[1]
    ori = init[2]
    policy2D[x][y] = policy[ori][x][y]
    
    while policy[ori][x][y] != '*':
        if policy[ori][x][y] == '#':
            o2 = ori
        elif policy[ori][x][y] == 'R':
            o2 = (ori - 1) % 4
        elif policy[ori][x][y] == 'L':
            o2 = (ori - 1) % 4
        x = x + forward[o2][0]
        y = y + forward[o2][1]
        ori = o2
        policy2D[x][y] = policy[ori][x][y]
    return policy2D

p = optimum_policy2D(grid, init, goal, cost)
for i in range(len(p)):
    print(p[i])