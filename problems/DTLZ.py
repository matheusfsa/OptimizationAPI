"""
Classes que representam os problemas DTLZ
Artigo: DEB, Kalyanmoy et al. Scalable test problems for evolutionary multiobjective optimization.
In: Evolutionary multiobjective optimization. Springer, London, 2005. p. 105-145.

"""
from problems.Problem import Problem
import numpy as np


class DTLZ(Problem):

    def __init__(self, n, m):
        super(DTLZ, self).__init__(n, m)
        self.k = n - m + 1

    def g(self, X):
        raise NotImplementedError("Should have implemented this")

    def get_upper_lower(self):
        return np.ones(self.n), np.zeros(self.m)


class DTLZ1(DTLZ):
    def g(self, X):
        XM = X[:, self.n - self.k:]
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
        g = np.reshape(1 + self.g(X), (1, -1))
        res = np.zeros((X.shape[0], self.m))
        for i in range(self.m):
            if i == 0:
                res[:, i] = 0.5 * np.multiply(np.prod(X[:, :self.m-(i+1)], axis=1), g)
            elif i != self.m-1:
                a1 = np.prod(X[:, :self.m-(i+1)], axis=1)
                a2 = np.reshape(1 - X[:, self.m-(i+1)], (1, -1))
                a = np.multiply(a1, a2)
                res[:, i] = 0.5*np.multiply(a, g)
            else:
                a = np.reshape(1 - X[:, self.m - (i + 1)], (1, -1))
                res[:, i] = 0.5*np.multiply(a, g)
        return res


class DTLZ2(DTLZ):


    def g(self, X):
        XM = X[:, self.n - self.k:]
        vec = XM - 0.5
        return np.sum(np.power(vec, 2), axis=1)

    def evaluate(self, X):
        if type(X) != np.ndarray:
            X = np.array(X)
            if len(X.shape) == 1:
                X = np.reshape(X, [1, X.shape[0]])
        g = np.reshape(1 + self.g(X), (1, -1))
        res = np.zeros((X.shape[0], self.m))
        X2 = np.dot(np.pi/2, X[:, :self.m - 1])
        for i in range(self.m):
            if i == 0:
                a = np.prod(np.cos(X2), axis=1)
            elif i != self.m - 1:
                a = X2.copy()
                a[:, :self.m - (i+1)] = np.cos(a[:, :self.m - (i+1)])
                a[:, self.m - (i+1)] = np.sin(a[:, self.m - (i+1)])
                a = np.prod(a, axis=1)
            else:
                a = np.sin(X2[:, 0])
            res[:, i] = np.multiply(g, a)
        return res


class DTLZ3(DTLZ):

    def g(self, X):

        XM = X[:, self.n - self.k:]
        vec = XM - 0.5
        scalar = 20 * np.pi
        right = np.cos(np.dot(scalar, XM))
        left = np.power(vec, 2)
        a = left - right
        return 100 * (self.k + np.sum(a, axis=1))

    def evaluate(self, X):
        if type(X) != np.ndarray:
            X = np.array(X)
            if len(X.shape) == 1:
                X = np.reshape(X, [1, X.shape[0]])
        g = np.reshape(1 + self.g(X), (1, -1))
        res = np.zeros((X.shape[0], self.m))
        X2 = np.dot(np.pi/2, X[:, :self.m - 1])

        for i in range(self.m):
            if i == 0:
                a = np.prod(np.cos(X2), axis=1)
            elif i != self.m - 1:
                a = X2.copy()
                a[:, :self.m - (i+1)] = np.cos(a[:, :self.m - (i+1)])
                a[:, self.m - (i+1)] = np.sin(a[:, self.m - (i+1)])
                a = np.prod(a, axis=1)
            else:
                a = np.sin(X2[:, 0])
            res[:, i] = np.multiply(g, a)
        return res


class DTLZ4(DTLZ):

    def g(self, X):
        XM = X[:, self.n - self.k:]
        vec = XM - 0.5
        return np.sum(np.power(vec, 2), axis=1)

    def evaluate(self, X):
        alpha = 100
        if type(X) != np.ndarray:
            X = np.array(X)
            if len(X.shape) == 1:
                X = np.reshape(X, [1, X.shape[0]])
        g = np.reshape(1 + self.g(X), (1, -1))
        res = np.zeros((X.shape[0], self.m))
        X2 = np.dot(np.pi/2, np.power(X[:, :self.m - 1], alpha))
        for i in range(self.m):
            if i == 0:
                a = np.prod(np.cos(X2), axis=1)
            elif i != self.m - 1:
                a = X2.copy()
                a[:, :self.m - (i+1)] = np.cos(a[:, :self.m - (i+1)])
                a[:, self.m - (i+1)] = np.sin(a[:, self.m - (i+1)])
                a = np.prod(a, axis=1)
            else:
                a = np.sin(X2[:, 0])
            res[:, i] = np.multiply(g, a)
        return res



