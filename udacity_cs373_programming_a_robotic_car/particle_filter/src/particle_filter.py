from math import *
import random

landmarks = [[20.0, 20.0],  # 設定地標作為之後感知（sense）的依據
              [80.0, 80.0],
              [20.0, 80.0],
              [80.0, 20.0]]
world_size = 100.0  # 在此例中世界的寬度是100m x 100m

class robot:  # 定義粒子的class
    def __init__(self):  # 建立這個類別的物件時的初始化函式
        self.x = random.random() * world_size  # 預設x位置
        self.y = random.random() * world_size  # 預設y位置
        self.orientation = random.random() * 2.0 * pi  # 預設粒子朝向的方向
        self.forward_noise = 0.0  # 設定前進時的模糊參數
        self.turn_noise = 0.0  # 設定轉彎時的模糊參數
        self.sense_noise = 0.0  # 設定感知時的模糊參數
        
    def set(self, x, y, orientation):  # 重設粒子的x，y，orientation
        if x < 0 or x >= world_size:  # 確認設定的x，y，orientation符合規定範圍
            raise ValueError('X coordinate out of bound')  #
        if y < 0 or y >= world_size:  #
            raise ValueError('Y coordinate out of bound')  #
        if orientation < 0 or orientation >= 2 * pi:  #
            raise ValueError('Orientation must be in [0..2pi]')  #
        self.x = float(x)  # 設定粒子的x，y，orientation
        self.y = float(y)  #
        self.orientation = float(orientation)  #
    def set_noise(self, f_noise, t_noise, s_noise):  # 重設粒子的噪音係數
        self.forward_noise = float(f_noise)  # 設定前進，轉彎，感知時的噪音係數
        self.turn_noise = float(t_noise)  #
        self.sense_noise = float(s_noise)  #
    def sense(self):  # 獲取粒子與各個地標的距離
        result = []  #
        for i in range(len(landmarks)):  # 遍歷每個地標
            dist = sqrt((self.x - landmarks[i][0]) ** 2 + (self.y - landmarks[i][1]) ** 2)  # 取得直線距離
            dist += random.gauss(0.0, self.sense_noise)  # 加入高斯噪音
            result.append(dist)  # 存入陣列
        return result  #
    def move(self, turn, forward):
        if forward < 0:
            raise ValueError('Robot cant move backwards')
        orientation = self.orientation + float(turn) + random.gauss(0.0, self.turn_noise)
        orientation %= 2 * pi
        dist = float(forward) + random.gauss(0.0, self.forward_noise)
        x = self.x + (cos(orientation) * dist)
        y = self.y + (sin(orientation) * dist)
        x %= world_size
        y %= world_size
        res = robot()
        res.set(x, y, orientation)
        res.set_noise(self.forward_noise, self.turn_noise, self.sense_noise)
        return res
    def Gaussian(self, mu, sigma, x):
        return exp(-((mu - x) ** 2) / (sigma ** 2) / 2.0) / sqrt(2.0 * pi * (sigma ** 2))

    def measurement_prob(self, measurement):
        prob = 1.0;
        for i in range(len(landmarks)):
            dist = sqrt((self.x - landmarks[i][0]) ** 2 + (self.y - landmarks[i][1]) ** 2)
            prob *= self.Gaussian(dist, self.sense_noise, measurement[i])
        return prob
    def __repr__(self):  # 回傳粒子的資訊組成的字串
            return '[x=%.6s y=%.6s orient=%.6s]' % (str(self.x), str(self.y), str(self.orientation))  #
    
    def eval(self, robot, particles):  #
        sum = 0.0;  #
        for i in range(len(particles)):  # 遍歷所有粒子
            dx = (particles[i].x - robot.x + (world_size / 2.0)) % world_size - (world_size / 2.0)  # 計算x和y的差，此處因為世界是循環的，0再
            dy = (particles[i].y - robot.y + (world_size / 2.0)) % world_size - (world_size / 2.0)  # 減就變99所以需要根據word_size做一些調整
                                                    # 現時情況就與目標值相減即可
            err = sqrt(dx * dx + dy * dy)  # 計算歐幾里得距離
            sum += err  # 加總誤差
        return sum / float(len(particles))  # 除以粒子個數
    
    def resample(self, weights, particles):  # 重新採樣粒子
        result = []  #
        beta = 0.0  #
        max_w = max(weights)  #
        l = len(weights)
        index = int(random.random() * l)  #
        for i in range(l):  #
            beta += random.random() * 2.0 * max_w  #
            while beta > weights[index]:  #
                beta -= weights[index]  #
                index = (index + 1) % l  #
            result.append(particles[index])  #
        return result  #
x = robot()
print((0 - 99 + 50) % 100 - 50)
print((99 - 0 + 50) % 100 - 50)
print(x.Gaussian(0, 1, 0))
