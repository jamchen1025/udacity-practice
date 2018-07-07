grid = [[0, 0, 0, 0],
           [0, 0, 0, 0],
           [0, 0, 0, 0],
           [0, 1, 1, 0]]
# grid = [[0, 0,  0],
#            [0, 0, 0]]
goal = [0, len(grid[0]) - 1]
cost = 1
delta = [[-1, 0 ],  # go up
             [ 0, -1],  # go left
             [ 1, 0 ],  # go down
             [ 0, 1 ]]  # go right
delta_name = ['^', '<', 'v', '>']
hit_cost = 100.0
s_prob = 0.5
f_prob = (1.0 - s_prob) / 2.0
def stoc_value(grid, goal, cost, hit_cost, s_prob, f_prob):
    value = [[hit_cost for i in range(len(grid[0]))] for j in range(len(grid))]
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
                        v2 = cost
                        for i in range(-1,2):
                            a2 = (a + i) % 4
                            x2 = x + delta[a2][0]
                            y2 = y + delta[a2][1]
                            if i == 0:
                                p2 = s_prob
                            else:
                                p2 = f_prob
                            if x2 >= 0 and x2 < len(grid) and y2 >= 0 and y2 < len(grid[0]) and grid[x2][y2] == 0:
                                v2 += p2 * value[x2][y2]
                            else:
                                v2 += p2 * hit_cost  
                        if v2 < value[x][y]:
                            value[x][y] = v2
                            policy[x][y] = delta_name[a]
                            change = True
    return value, policy

value, policy = stoc_value(grid, goal, cost, hit_cost, s_prob, f_prob)

for i in range(len(value)):
    print(value[i])
print('-------')
for i in range(len(policy)):
    print(policy[i])