import numpy as np


class SBXCrossover():
    def __init__(self, distribution_index=20, probability=0.9, upper=np.ones(12), lower=np.zeros(12)):
        self.distribution_index= distribution_index
        self.probability = probability
        self.lower = lower
        self.upper = upper
        self.eps = np.exp(-14)

    def execute(self, sol1, sol2):
        x1= sol1.copy()
        x2 = sol2.copy()

        if np.random.rand() < self.probability:
            for i in range(x1.shape[0]):
                vx1 = x1[i].copy()
                vx2 = x2[i].copy()
                if np.random.rand() < 0.5:
                    if np.abs((vx1-vx2)> self.eps):
                        if vx1 < vx2:
                            y1, y2 = vx1, vx2
                        else:
                            y1, y2 = vx2, vx1
                        rand = np.random.rand()
                        beta = 1.0 + (2.0 * (y1 - self.lower[i]) / (y2 - y1))
                        alpha = 2.0 - beta ** -(self.distribution_index + 1.0)
                        if rand <= (1.0 / alpha):
                            betaq = np.power(rand * alpha, (1.0 / (self.distribution_index + 1.0)))
                        else:
                            betaq = np.power(1.0 / (2.0 - rand * alpha), 1.0 / (self.distribution_index + 1.0))
                        c1 = 0.5 * (y1 + y2 - betaq * (y2 - y1))
                        beta = 1.0 + (2.0 * (self.upper[i] - y2) / (y2 - y1))
                        alpha = 2.0 - np.power(beta, -(self.distribution_index + 1.0))
                        if rand <= (1 / alpha):
                            betaq = np.power((rand * alpha), (1.0 / (self.distribution_index + 1.0)))
                        else:
                            betaq = np.power(1.0 / (2.0 - rand * alpha), 1.0 / (self.distribution_index + 1.0))
                        c2 = 0.5 * (y1 + y2 + betaq * (y2 - y1))
                        c1 = self.trunca(c1, i)
                        c2 = self.trunca(c2, i)
                        if np.random.rand() <= 0.5:
                            x1[i] = c2
                            x2[i] = c1
                        else:
                            x1[i] = c1
                            x2[i] = c2
        return x1, x2

    def trunca(self, s, i):
        if s < self.lower[i]:
            s = self.lower[i]
        elif s > self.upper[i]:
            s = self.upper[i]
        return s

    def execute2(self, x1, x2):
        u = np.random.rand()
        if u <= 0.5:
            beta = (2*u)**(1/(self.nc+1))
        else:
            beta = (1/2*(1-u))**(1/(self.nc+1))
        x1_new = np.dot(0.5, np.dot(1 + beta, x1) + np.dot(1 - beta, x2))
        x2_new = np.dot(0.5, np.dot(1 - beta, x1) + np.dot(1 + beta, x2))
        return x1_new, x2_new


a = np.random.rand(12)
b = np.random.rand(12)