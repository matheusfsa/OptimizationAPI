import numpy as np
from time import *
from ctypes import *
import domModule
import pygmo as pg
from pyDOE import  *
def domina(s1, s2):
    best_is_one = False
    best_is_two = False
    for i in range(s1.shape[0]):
        if s1[i] < s2[i]:
            best_is_one = True
            if best_is_two:
                return 0
        elif s2[i] < s1[i]:
            best_is_two = True
            if best_is_one:
                return 0
    if best_is_one and not best_is_two:
        return 1
    if best_is_two and not best_is_one:
        return -1
    return 0


def dominaC(s1, s2):
    return domModule.dominance(s1.tolist(), s2.tolist())


def fnds(Y,func):
        F = [[]]
        S = [[] for _ in range(Y.shape[0])]
        n = np.zeros(Y.shape[0])
        for i in range(Y.shape[0]-1):
            for j in range(i+1, Y.shape[0]):
                if i != j:
                    dom = func(Y[i], Y[j])
                    if dom == 1:
                        S[i].append(j)
                        n[j] += 1
                    elif dom == -1:
                        n[i] += 1
                        S[j].append(i)

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


def getNonDominatedSolutions(X, Y):
    F = []
    n = np.zeros(X.shape[0])
    for i in range(X.shape[0] - 1):
        for j in range(i + 1, X.shape[0]):
            if i != j:
                dom = domina(Y[i], Y[j])
                if dom == 1:
                    n[j] += 1
                elif dom == -1:
                    n[i] += 1
        if n[i] == 0:
            F.append(i)

    return X[F], Y[F]


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


def calcula_tempo(func):
    pop = lhs(3, 100)
    ini = time()
    f1 = fnds(pop,func)
    print('meu fnds: ', time() - ini)
    ini = time()
    f2, _, _, _ = pg.fast_non_dominated_sorting(points=pop)
    print('pygmo fnds: ', time() - ini)
    return f1, f2