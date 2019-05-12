import time
class EvolutionaryAlgorithm(object):


    def createInitialPopulation(self):
        raise NotImplementedError("Should have implemented this")

    def evaluatePopulation(self, population):
        raise NotImplementedError("Should have implemented this")

    def isStoppingConditionReached(self):
        raise NotImplementedError("Should have implemented this")

    def selection(self, population, fitness, offspring_population, fitness_offspring):
        raise NotImplementedError("Should have implemented this")

    def reproduction(self, population):
        raise NotImplementedError("Should have implemented this")

    def initProgress(self):
        raise NotImplementedError("Should have implemented this")

    def updateProgress(self):
        raise NotImplementedError("Should have implemented this")

    def getNonDominatedSolutions(self, population, fitness):
        raise NotImplementedError("Should have implemented this")

    def execute(self):
        inicio = time.time()
        population = self.createInitialPopulation()
        fitness = self.evaluatePopulation(population)
        self.initProgress()
        while not self.isStoppingConditionReached():
            offspring_population = self.reproduction(population)
            fitness_offspring = self.evaluatePopulation(offspring_population)
            population, fitness = self.selection(population, fitness, offspring_population, fitness_offspring)
            self.updateProgress()
        print('Execution time: ', (time.time() - inicio), 's')
        return self.getNonDominatedSolutions(population, fitness)