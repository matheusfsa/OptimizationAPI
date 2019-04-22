"""
Classes que representam os problemas DTLZ
Artigo: DEB, Kalyanmoy et al. Scalable test problems for evolutionary multiobjective optimization.
In: Evolutionary multiobjective optimization. Springer, London, 2005. p. 105-145.

"""
from problems.Problem import Problem
import numpy as np


class DTLZ1(Problem):

    def __init__(self, n, m):
        self.n = n
        self.m = m
        self.k = n - m + 1
        self.test()

    def g(self, XM):
        vec = XM - 0.5
        scalar = 20*np.pi
        right = np.cos(np.dot(scalar, XM))
        left = np.power(vec, 2)
        a = left - right
        return 100*(self.k + np.sum(a, axis=1))

    def evaluate(self, X):
        if type(X) != np.ndarray:
            X = np.array(X)
            if len(X.shape) == 1:
                X = np.reshape(X, [1, X.shape[0]])
        XM = X[:, self.n - self.k:]
        g = np.reshape(1 + self.g(XM), (1, -1))
        res = np.zeros((X.shape[0], self.m))
        for i in range(self.m):

            if i == 0:
                res[:, i] = 0.5 * np.multiply(np.prod(X[:, :self.m-(i+1)], axis=1), g)
                print(np.multiply(np.prod(X[:, :self.m-(i+1)]), g))
            elif i != self.m-1:

                a1 = np.prod(X[:, :self.m-(i+1)], axis=1)
                a2 = np.reshape(1 - X[:, self.m-(i+1)], (1, -1))
                a = np.multiply(a1, a2)
                res[:, i] = 0.5*np.multiply(a, g)
            else:
                a = np.reshape(1 - X[:, self.m - (i + 1)], (1, -1))
                res[:, i] = 0.5*np.multiply(a, g)

        return res

    def test(self):
        X = [[0.1, 0.4, 0.9, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5]]
        print(self.evaluate(X))


DTLZ1(12,3)