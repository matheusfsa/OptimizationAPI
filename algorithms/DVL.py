from pyDOE import *
from pygmo import *
from sklearn import linear_model
import pandas as pd
import numpy as np
from sklearn.metrics import mean_squared_error
import problems.DTLZ as dtlz
import os

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'


class DVL(object):

    def __init__(self, problem, dataset_generator, ini_dataset_size, estimator, epsilon, max_iteractions, pop_size):
        self.problem = problem
        self.dataset_generator = dataset_generator
        self.estimator = estimator
        self.epsilon = epsilon
        self.max_iteractions = max_iteractions
        self.pop_size = pop_size
        self.ini_dataset_size = ini_dataset_size





    def execute(self):
        X, Y = self.dataset_generator(self.problem, self.ini_dataset_size)
        erro_min = np.inf
        i = 0
        erro = 100
        pop, ev_pop, erro, erro_hv = self.estimator(X, Y, self.problem,self.ini_dataset_size, 0)
        while erro < erro_min and i < self.max_iteractions:
            X_min = X

            Y_min = Y
            X = pop
            Y = ev_pop
            erro_min = erro
            pop, ev_pop, erro, erro_hv = self.estimator(X, Y, self.problem, self.ini_dataset_size, 0)
            print(pd.DataFrame(pop).describe())
            i = i + 1
        print("número de iterações: ", i)
        return self.estimator(X_min, Y_min, self.problem, self.pop_size, 1), pd.DataFrame(X_min), pd.DataFrame(Y_min), pd.DataFrame(X), pd.DataFrame(Y)


def getNonDominateSolutions(X, y):
    def domina(s1, s2):
        k1 = 0
        k2 = 0
        for i in range(y.shape[1]):
            if s1[i] < s2[i]:
                k1 += 1
            elif s2[i] < s1[i]:
                k2 += 1
        if k1 > 0 and k2 == 0:
            return 1
        if k2 > 0 and k1 == 0:
            return -1
        return 0
    SX = np.empty((0, X.shape[1]))
    Sy = np.empty((0, y.shape[1]))
    for i in range(X.shape[0]):
        n_p = 0
        for j in range(X.shape[0]):
            dom = domina(y[i], y[j])
            if dom == -1:
                n_p += 1
                break
        if n_p == 0:
            SX = np.append(SX, [X[i]], axis=0)
            Sy = np.append(Sy, [y[i]], axis=0)

    return SX, Sy


def train_model(x, y, n):
    est = linear_model.RidgeCV(alphas=[0.05, 0.1, 0.3, 1, 3, 5, 10, 15, 30, 50, 75])
    model = est
    model.fit(x, y)
    return model


def columns_vars(n, m):
    vetor = ['Obj_' + str(i) for i in range(m)]
    res = []
    for i in range(n):
        vx = vetor.copy()
        for j in range(i):
            vx.append('Var_' + str(j))
        res.append(vx)
    return res


def trunca(s, lower, upper):
    for i in range(len(s)):
        if s[i] < lower[i]:
            s[i] = lower[i]
        elif s[i] > upper[i]:
            s[i] = upper[i]
    return s


def lhs_estimator(X, Y, problem, pop_size, op):
    if op == 0:
        ref_points = lhs(problem.m, samples=pop_size)
    else:
        ref_points = np.loadtxt('/home/matheus/PycharmProjects/OptimizationAPI/algorithms/Pontos.txt')

    train_points = pd.DataFrame(Y)
    train_sols = pd.DataFrame(X)
    train_sols.columns = ['Var_' + str(i) for i in range(train_sols.shape[1])]
    train_points.columns = ['Obj_' + str(i) for i in range(train_points.shape[1])]

    data = pd.concat([train_points, train_sols], axis=1)
    columns = columns_vars(problem.n, problem.m)
    reg = [train_model(data[columns[i]], data['Var_' + str(i)], 500) for i in range(problem.n)]
    pop = []
    for i in range(pop_size):
        sol = []
        for j in range(problem.n):
            vetor = [ref_points[i][j] for j in range(problem.m)]
            for k in range(j):
                vetor.append(sol[k])
            v = reg[j].predict(np.reshape(vetor, (1, -1)))
            if v > 1:
                v = np.array([1])
            elif v < 0:
                v = np.array([0])
            sol.append(v[0])
        pop.append(sol)

    pop = np.array(pop)
    ev_pop = problem.evaluate(pop)
    error = mean_squared_error(ev_pop, ref_points)
    if op == 1:
        # pop, ev_pop = getNonDominateSolutions(pop, ev_pop)
        print('Tamanho da população resultante: ', pop.shape[0])
    diff = 0
    try:
        hv_ref = calcula_hv_pop(ref_points)
        hv_est = calcula_hv_pop(ev_pop)
        if op == 1:
            print('HV_est: ', hv_est)
        diff = hv_ref - hv_est
    except ValueError:
        diff = 0
    return pop, ev_pop, error, diff


def calcula_hv_pop(pop):
    ref_point = [2, 2, 2]
    hv = hypervolume(pop)
    return hv.compute(ref_point) / np.prod(ref_point)


def lhs_generator(problem, size):
    k = lhs(problem.n, samples=size)
    return k, problem.evaluate(k)


dvl1 = DVL(dtlz.DTLZ1(12, 3), lhs_generator, 5000, lhs_estimator, 0.001, 20, 91)


def test():
    its = [500, 1000, 5000, 10000, 15000, 20000, 25000]
    for i in its:
        print('')
        print('---------------------------------------------')
        print('tamanho: ', i)
        print('')
        res = DVL(dtlz.DTLZ2(12, 3), lhs_generator, i, lhs_estimator, 0.001, 10, 91).execute()
        print("Erro de estimação:", res[2])
        print("Erro hv: ", res[3])


#test()