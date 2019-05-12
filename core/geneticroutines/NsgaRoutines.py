import numpy as np
from time import *

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


def fnds(X, Y):
        inicio = time()
        F = [[]]
        S = [[] for _ in range(X.shape[0])]
        n = np.zeros(X.shape[0])
        #print('inicialização: ', time() - inicio)
        #inicio = time()
        #resto = 0
        #dom_time = 0
        for i in range(X.shape[0]-1):
            for j in range(i+1, X.shape[0]):
                if i != j:
                    #inicio = time()
                    dom = domina(Y[i], Y[j])
                    #dom_time += time() - inicio
                    inicio = time()
                    if dom == 1:
                        S[i].append(j)
                        n[j] += 1
                    elif dom == -1:
                        n[i] += 1
                        S[j].append(i)
                    #resto += time() - inicio

            if n[i] == 0:
                F[0].append(i)
        #print('dom_time: ', dom_time)
        #print('resto:', resto)
        #print('for: ', time() - inicio)
        #inicio = time()
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
        #print('while: ', time() - inicio)
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