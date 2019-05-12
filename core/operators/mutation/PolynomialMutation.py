import numpy as np


class PolynomialMutation:
    def __init__(self, mutation_probability=1/12, distribution_index=20, lower=np.zeros(12), upper=np.ones(12)):
        self.distribution_index = distribution_index
        self.lower = lower
        self.upper = upper
        self.mutation_probability = mutation_probability

    def l(self, u):
        return (2*u)**(1/(1+self.nm))

    def r(self, u):
        return 1 - (2*(1 - u)) ** (1/(1+self.nm))

    def execute(self, solucao):
        p = solucao.copy()
        for i in range(p.shape[0]):
            if np.random.rand() <= self.mutation_probability:
                y = p[i]
                yl = self.lower[i]
                yu = self.upper[i]
                delta1 = (y - yl) / (yu - yl)
                delta2 = (yu - y) / (yu - yl)
                rnd = np.random.rand()
                mutPow = 1.0 / (self.distribution_index + 1.0)
                if rnd <= 0.5:
                    xy = 1.0 - delta1
                    val = 2.0 * rnd + (1.0 - 2.0 * rnd) * (xy ** (self.distribution_index + 1.0))
                    deltaq = val ** mutPow - 1.0
                else:
                    xy = 1.0 - delta2
                    val = 2.0 * (1.0 - rnd) + 2.0 * (rnd - 0.5) * (xy ** (self.distribution_index + 1.0))
                    deltaq = 1.0 - val ** mutPow
                y += deltaq * (yu - yl)
                if yl > y:
                    y = yl
                elif y > yu:
                    y = yu
                p[i] = y
        return p


