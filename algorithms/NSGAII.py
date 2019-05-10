from algorithms.EvolutionaryAlgorithm import EvolutionaryAlgorithm
import numpy as np

class NSGAII(EvolutionaryAlgorithm):

    def __init__(self, max_iteractions, problem, crossover_operator, mutation_operator,
                 selection_operator):
        self.max_iteractions = max_iteractions
        self.problem = problem
        self.crossover_operator = crossover_operator
        self.mutation_operator = mutation_operator
        self.selection_operator = selection_operator

    def fnds(self, X, Y):
        def domina(s1, s2):
            k1 = 0
            k2 = 0
            for i in range(Y.shape[1]):
                if s1[i] < s2[i]:
                    k1 += 1
                elif s2[i] < s1[i]:
                    k2 += 1
            if k1 > 0 and k2 == 0:
                return 1
            if k2 > 0 and k1 == 0:
                return -1
            return 0
        S = [[] for _ in range(X.shape[0])]
        n = np.zeros(X.shape[0])
        for i in range(X.shape[0]):
            for j in range(X.shape[0]):
                if i != j:
                    dom = domina(Y[i], Y[j])
                    if dom == 1:
                        S[i].append(j)
                    elif dom == -1:
                        n[i] += 1
        return S, n

def domina(s1, s2):
    k1 = 0
    k2 = 0
    for i in range(s1.shape[0]):
        if s1[i] < s2[i]:
            k1 += 1
        elif s2[i] < s1[i]:
            k2 += 1
    if k1 > 0 and k2 == 0:
        return 1
    if k2 > 0 and k1 == 0:
        return -1
    return 0


def fnds(X, Y):

        F = [[]]
        S = [[] for _ in range(X.shape[0])]
        n = np.zeros(X.shape[0])
        for i in range(X.shape[0]):
            for j in range(X.shape[0]):
                if i != j:
                    dom = domina(Y[i], Y[j])
                    if dom == 1:
                        S[i].append(j)
                    elif dom == -1:
                        n[i] += 1
            if n[i] == 0:
                F[0].append(i)
        i = 0
        while F[i]:
            Q = []
            for p in F[i]:
                for q in S[p]:
                    n[q] = n[q] - 1
                    if n[q] == 0:
                        Q.append(q)
            i += 1
            F.append(Q)
        return F


def crowding_distance_assignment(Y):
    l = Y.shape[0]
    I = np.zeros(Y.shape[0])
    a = np.arange(Y.shape[0]).reshape((-1, 1))
    Ys = np.append(Y, a, axis=1)
    for m in range(Y.shape[1]):
        Ys = Ys[Ys[:, m].argsort()]
        I[0] = np.inf
        I[l-1] = np.inf
        for i in range(1, l-2):
            I[i] = I[i] + (Ys[i+1, m] - Ys[i-1, m])/(Ys[l-1, m] - Ys[0, m])
    return I

X = np.zeros((3,3))
Y = np.array([[1,1,1], [0.5,0.5,0.5],[0,0,0]])
res = fnds(X,Y)
res2 = crowding_distance_assignment(Y)