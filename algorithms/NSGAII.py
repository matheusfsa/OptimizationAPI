from algorithms.EvolutionaryAlgorithm import EvolutionaryAlgorithm
import numpy as np
import  pygmo as pg
from core.geneticroutines.NsgaRoutines import *
from core.operators.crossover.SBXCrossover import *
from core.operators.mutation.PolynomialMutation import *
from problems.DTLZ import *
from time import *
class NSGAII(EvolutionaryAlgorithm):

    def __init__(self, max_iterations=100, problem=DTLZ2(12, 3), crossover_operator=SBXCrossover(),
                 mutation_operator=PolynomialMutation(), max_population_size=100):
        self.max_iterations = max_iterations
        self.problem = problem
        self.crossover_operator = crossover_operator
        self.mutation_operator = mutation_operator
        self.max_population_size = max_population_size
        self.t = 0

    def initProgress(self):
        self.t = 0

    def updateProgress(self):
        self.t += 1

    def isStoppingConditionReached(self):
        return self.t == self.max_iterations

    def evaluatePopulation(self, population):
        return self.problem.evaluate(population)

    def getNonDominatedSolutions(self, population, fitness):
        return getNonDominatedSolutions(population, fitness)

    def selection(self, PX, PY, QX, QY):

        RX, RY = np.append(PX, QX, axis=0), np.append(PY, QY, axis=0)
        F = fnds(RY, dominaC)
        SX, SY = np.empty((0, self.problem.n)), np.empty((0, self.problem.m))

        i = 0
        l = len(F[i])
        while SX.shape[0] + l <= self.max_population_size:
            SX, SY = np.append(SX, RX[F[i]], axis=0), np.append(SY, RY[F[i]], axis=0)
            i += 1
            l = len(F[i])
        delta = self.max_population_size - SX.shape[0]

        if delta != 0:
            I = crowding_distance_assignment(RY[F[i]])
            f = np.array(F[i])
            F[i] = f[I.argsort()]
            F[i] = F[i][l-delta:]
            SX, SY = np.append(SX, RX[F[i]], axis=0), np.append(SY, RY[F[i]], axis=0)

        return SX, SY

    def createInitialPopulation(self):
        X = np.random.rand(self.max_population_size, self.problem.n)
        return X

    def reproduction(self, X):
        NX = np.empty((0, X.shape[1]))
        for i in range(0, X.shape[0], 2):
            cx1, cx2 = self.crossover_operator.execute(X[i], X[i+1])
            cx1 = self.mutation_operator.execute(cx1)
            cx2 = self.mutation_operator.execute(cx2)
            NX = np.append(NX, [cx1,cx2], axis=0)
        return NX


NSGAII(max_iterations=1, max_population_size=100).execute()




