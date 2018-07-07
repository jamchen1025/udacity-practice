import random
import numpy as np
import matplotlib.pyplot as plt

class Robot(object):
    def __init__(self, length=20.0):
        self.x = 0.0
        self.y = 0.0
        self.orientation = 0.0
        self.length = length
        self.steering_noise = 0.0
        self.distance_noise = 0.0
        self.steering_drift = 0.0

    def set(self, x, y, orientation):
        self.x = x
        self.y = y
        self.orientation = orientation % (2.0 * np.pi)

    def set_noise(self, steering_noise, distance_noise):
        self.steering_noise = steering_noise
        self.distance_noise = distance_noise

    def set_steering_drift(self, drift):
        self.steering_drift = drift

    def __repr__(self):
        return '[x=%.5f y=%.5f orient=%.5f]' % (self.x, self.y, self.orientation)
    
    def move(self, steering, distance, tolerance=0.001, max_steering_angle=np.pi / 4.0):
        if steering > max_steering_angle:
            steering = max_steering_angle
        if steering < -max_steering_angle:
            steering = -max_steering_angle
        if distance < 0.0:
            distance = 0.0

        steering2 = random.gauss(steering, self.steering_noise)
        distance2 = random.gauss(distance, self.distance_noise)
        steering2 += self.steering_drift

        turn = np.tan(steering2) * distance2 / self.length
        if abs(turn) < tolerance:
            self.x += distance2 * np.cos(self.orientation)
            self.y += distance2 * np.sin(self.orientation)
            self.orientation = (self.orientation + turn) % (2.0 * np.pi)
        else:
            radius = distance2 / turn
            cx = self.x - (np.sin(self.orientation) * radius)
            cy = self.y + (np.cos(self.orientation) * radius)
            self.orientation = (self.orientation + turn) % (2.0 * np.pi)
            self.x = cx + (np.sin(self.orientation) * radius)
            self.y = cy - (np.cos(self.orientation) * radius)


############## ADD / MODIFY CODE BELOW ####################
# ------------------------------------------------------------------------
#
# run - does a single control run


def make_robot():
    robot = Robot()
    robot.set(0, 1, 0)
    robot.set_steering_drift(0 / 180 * np.pi)
    return robot


# NOTE: We use params instead of tau_p, tau_d, tau_i
def run(robot, params, n=100, speed=1.0):
    x_trajectory = []
    y_trajectory = []
    err = 0
    prev_cte = robot.y
    int_cte = 0
    for i in range(2 * n):
        cte = robot.y
        diff_cte = cte - prev_cte
        int_cte += cte
        prev_cte = cte
        steer = -params[0] * cte - params[1] * diff_cte - params[2] * int_cte
        robot.move(steer, speed)
        x_trajectory.append(robot.x)
        y_trajectory.append(robot.y)
        if i >= n:
            err += cte ** 2
    return x_trajectory, y_trajectory, err / n


# Make this tolerance bigger if you are timing out!

def twiddle(tol=0.00001):
    p = [0, 0, 0]
    dp = [0.5, 1, 0.01]
    robot = make_robot()
    x_trajectory, y_trajectory, best_err = run(robot, p)
    ixx = 0
    xx = []
    yyp = []
    yyi = []
    yyd = []
    xx.append(ixx)
    yyp.append(p[0])
    yyd.append(p[1])
    yyi.append(p[2])
    ixx += 1
    it = 0
    while sum(dp) > tol:
        for i in range(len(p)):
            p[i] += dp[i]
            robot = make_robot()
            x_trajectory, y_trajectory, err = run(robot, p)
            print("a i= {} it = {} good? ={} best error = {} error ={} pid {}".format(i, it, (err < best_err), best_err, err, p))
            xx.append(ixx)
            yyp.append(p[0])
            yyd.append(p[1])
            yyi.append(p[2])
            ixx += 1
            if err < best_err:
                best_err = err
                dp[i] *= 1.1
            else:
                p[i] -= 2 * dp[i]
                robot = make_robot()
                x_trajectory, y_trajectory, err = run(robot, p)
                print("b i= {} it = {} good? ={} best error = {}  error ={}  pid {}".format(i, it, (err < best_err), best_err, err, p))
                xx.append(ixx)
                yyp.append(p[0])
                yyd.append(p[1])
                yyi.append(p[2])
                ixx += 1
                if err < best_err:
                    best_err = err
                    dp[i] *= 1.1
                else:
                    p[i] += dp[i]
                    dp[i] *= 0.9
                
        it += 1
    return p, xx, yyp, yyd, yyi


params, xx, yyp, yyd, yyi = twiddle()
robot = make_robot()

x_trajectory, y_trajectory, err = run(robot, params)

n = len(x_trajectory)

plt.plot(x_trajectory, y_trajectory, 'g', label='twiddle PID controller')
plt.plot(x_trajectory, np.zeros(n), 'r', label='reference')
plt.legend()

plt.figure(2)
plt.plot(xx, yyp, 'r', label='p')
plt.plot(xx, yyd, 'g', label='d')
plt.plot(xx, yyi, 'b', label='i')
plt.show()
